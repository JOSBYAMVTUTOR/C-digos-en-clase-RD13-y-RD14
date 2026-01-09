import os
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    roc_auc_score, average_precision_score,
    classification_report, confusion_matrix
)
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import lightgbm as lgb
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import shap

# Para texto
try:
    from transformers import AutoTokenizer, AutoModel
    _HAS_TRANSFORMERS = True
except Exception:
    _HAS_TRANSFORMERS = False


CSV_PATH = "creditcard.csv"         
TARGET_COL = "Class"                
TEXT_COL = None                     

RANDOM_STATE = 42
TEST_SIZE = 0.2

# BERT si hay TEXT_COL
BERT_MODEL = "distilbert-base-uncased"
BERT_MAX_LEN = 128
BERT_BATCH = 16

# Autoencoder
AE_EPOCHS = 12
AE_BATCH = 512
AE_LR = 1e-3
AE_HIDDEN = 32
AE_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def load_csv(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"No existe: {path}")
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError("CSV vacio")
    return df


def get_bert_embeddings(texts: pd.Series, model_name: str) -> np.ndarray:
    if not _HAS_TRANSFORMERS:
        raise RuntimeError("Instala transformers para usar BERT: pip install transformers")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    model.eval()

    all_vecs = []
    with torch.no_grad():
        for i in range(0, len(texts), BERT_BATCH):
            batch = texts.iloc[i:i + BERT_BATCH].fillna("").astype(str).tolist()
            enc = tokenizer(
                batch,
                padding=True,
                truncation=True,
                max_length=BERT_MAX_LEN,
                return_tensors="pt"
            )
            out = model(**enc)
            last = out.last_hidden_state  
            attn = enc["attention_mask"].unsqueeze(-1).float()
            masked = last * attn
            summed = masked.sum(dim=1)
            counts = attn.sum(dim=1).clamp(min=1e-6)
            vecs = (summed / counts).cpu().numpy()
            all_vecs.append(vecs)

    return np.vstack(all_vecs)


def build_tabular_preprocessor(df: pd.DataFrame, target_col: str, text_col: str | None):
    feat_cols = [c for c in df.columns if c != target_col and c != text_col]

    num_cols = df[feat_cols].select_dtypes(include=["number"]).columns.tolist()
    cat_cols = [c for c in feat_cols if c not in num_cols]

    num_pipe = Pipeline([
        ("imp", SimpleImputer(strategy="median")),
        ("sc", StandardScaler())
    ])

    cat_pipe = Pipeline([
        ("imp", SimpleImputer(strategy="most_frequent")),
        ("ohe",  __import__("sklearn").preprocessing.OneHotEncoder(handle_unknown="ignore"))
    ])

    pre = ColumnTransformer(
        transformers=[
            ("num", num_pipe, num_cols),
            ("cat", cat_pipe, cat_cols),
        ],
        remainder="drop"
    )

    return pre, feat_cols


def train_lgbm(X_train, y_train, X_val, y_val):
    pos = float((y_train == 1).sum())
    neg = float((y_train == 0).sum())
    scale_pos = (neg / max(pos, 1.0))

    model = lgb.LGBMClassifier(
        n_estimators=1200,
        learning_rate=0.03,
        num_leaves=64,
        subsample=0.9,
        colsample_bytree=0.9,
        reg_lambda=2.0,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        class_weight=None,
        scale_pos_weight=scale_pos
    )

    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        eval_metric="auc",
        callbacks=[lgb.early_stopping(stopping_rounds=80, verbose=False)]
    )
    return model


def eval_probs(y_true, prob, tag="model"):
    auc = roc_auc_score(y_true, prob)
    ap = average_precision_score(y_true, prob)
    print(f"\n== {tag} ==")
    print(f"ROC AUC: {auc:.6f}")
    print(f"PR AUC : {ap:.6f}")

    thr = np.quantile(prob, 0.95)
    pred = (prob >= thr).astype(int)

    print("\nMatriz confusion (thr p95):")
    print(confusion_matrix(y_true, pred))
    print("\nReporte (thr p95):")
    print(classification_report(y_true, pred, digits=4))

class AutoEncoder(nn.Module):
    def __init__(self, n_in: int, hidden: int):
        super().__init__()
        self.enc = nn.Sequential(
            nn.Linear(n_in, hidden * 2),
            nn.ReLU(),
            nn.Linear(hidden * 2, hidden),
            nn.ReLU(),
        )
        self.dec = nn.Sequential(
            nn.Linear(hidden, hidden * 2),
            nn.ReLU(),
            nn.Linear(hidden * 2, n_in),
        )

    def forward(self, x):
        z = self.enc(x)
        out = self.dec(z)
        return out


def train_autoencoder(X_train_np: np.ndarray):
    x = torch.tensor(X_train_np, dtype=torch.float32)
    ds = TensorDataset(x)
    dl = DataLoader(ds, batch_size=AE_BATCH, shuffle=True, drop_last=False)

    model = AutoEncoder(n_in=x.shape[1], hidden=AE_HIDDEN).to(AE_DEVICE)
    opt = torch.optim.Adam(model.parameters(), lr=AE_LR)
    loss_fn = nn.MSELoss()

    model.train()
    for ep in range(1, AE_EPOCHS + 1):
        losses = []
        for (xb,) in dl:
            xb = xb.to(AE_DEVICE)
            opt.zero_grad()
            recon = model(xb)
            loss = loss_fn(recon, xb)
            loss.backward()
            opt.step()
            losses.append(loss.item())
        print(f"AE ep {ep}/{AE_EPOCHS} loss {np.mean(losses):.6f}")

    return model


def ae_scores(model: nn.Module, X_np: np.ndarray) -> np.ndarray:
    model.eval()
    x = torch.tensor(X_np, dtype=torch.float32).to(AE_DEVICE)
    with torch.no_grad():
        recon = model(x)
        err = ((recon - x) ** 2).mean(dim=1).detach().cpu().numpy()
    return err

def shap_explain_lgbm(model, X_sample, feature_names=None, max_rows=2000):
    if X_sample.shape[0] > max_rows:
        X_sample = X_sample[:max_rows]

    explainer = shap.TreeExplainer(model)
    sv = explainer.shap_values(X_sample)

    print("\nSHAP listo. Se abrira un grafico si el entorno lo permite.")
    try:
        shap.summary_plot(sv, X_sample, feature_names=feature_names, show=True)
    except Exception:
        print("No se pudo mostrar plot en este entorno.")

def main():
    df = load_csv(CSV_PATH)

    if TARGET_COL not in df.columns:
        raise ValueError(f"Falta target: {TARGET_COL}")

    if TEXT_COL is not None and TEXT_COL not in df.columns:
        raise ValueError(f"Falta texto: {TEXT_COL}")

    y = df[TARGET_COL].astype(int).values

    train_df, test_df = train_test_split(
        df, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    # BERT si aplica
    if TEXT_COL is not None:
        print("Generando embeddings BERT...")
        train_text = get_bert_embeddings(train_df[TEXT_COL], BERT_MODEL)
        test_text = get_bert_embeddings(test_df[TEXT_COL], BERT_MODEL)
    else:
        train_text, test_text = None, None

    # preprocesador tabular
    pre, feat_cols = build_tabular_preprocessor(df, TARGET_COL, TEXT_COL)

    X_train_tab = pre.fit_transform(train_df)
    X_test_tab = pre.transform(test_df)

    # concat texto si existe
    if train_text is not None:
        X_train = np.hstack([X_train_tab.toarray() if hasattr(X_train_tab, "toarray") else X_train_tab, train_text])
        X_test = np.hstack([X_test_tab.toarray() if hasattr(X_test_tab, "toarray") else X_test_tab, test_text])
        feat_names = None 
    else:
        X_train = X_train_tab
        X_test = X_test_tab
        feat_names = None

    y_train = train_df[TARGET_COL].astype(int).values
    y_test = test_df[TARGET_COL].astype(int).values

    # valid split
    X_tr, X_val, y_tr, y_val = train_test_split(
        X_train, y_train, test_size=0.2, random_state=RANDOM_STATE, stratify=y_train
    )

    # LightGBM
    print("\nEntrenando LightGBM...")
    lgbm = train_lgbm(X_tr, y_tr, X_val, y_val)

    prob_lgbm = lgbm.predict_proba(X_test)[:, 1]
    eval_probs(y_test, prob_lgbm, tag="LightGBM")

    # Autoencoder: entrena con normales
    print("\nEntrenando Autoencoder...")
    X_train_np = X_train.toarray() if hasattr(X_train, "toarray") else np.asarray(X_train)
    X_test_np = X_test.toarray() if hasattr(X_test, "toarray") else np.asarray(X_test)

    normal_mask = (y_train == 0)
    ae = train_autoencoder(X_train_np[normal_mask])
    score = ae_scores(ae, X_test_np)

    # normaliza score a prob 0-1
    score_norm = (score - score.min()) / (score.max() - score.min() + 1e-9)
    eval_probs(y_test, score_norm, tag="Autoencoder")

    # SHAP para LightGBM
    print("\nCorriendo SHAP para LightGBM...")
    X_shap = X_test_np[:2000]
    shap_explain_lgbm(lgbm, X_shap, feature_names=feat_names)

    print("\nListo.")

if __name__ == "__main__":
    main()
