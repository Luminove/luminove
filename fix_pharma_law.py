# -*- coding: utf-8 -*-
"""
薬機法リスク表現の置換
韓国機能性化粧品の「認証カテゴリ名」としての「シワ改善」「美白」はそのまま残し、
効能訴求としての使用のみ置換する。
"""
import re, glob, os

REPLACEMENTS = [
    ("美白の王様", "透明感ケアで注目される成分"),
    ("最強の抗酸化成分", "抗酸化ケアで知られる成分"),
    ("シミ改善", "シミ・くすみが気になる肌のケア"),
    ("肌再生", "肌コンディションを整えるケア"),
    ("リフティング効果", "ハリ感のある肌印象"),
    ("メラニン生成を抑制し", "メラニン生成に着目し"),
    ("角層の奥まで浸透", "角質層までうるおいを届ける"),
    ("深いうるおい", "うるおい感"),
    ("医師監修", "医師の知見を活かした商品選定"),
    ("医師推薦", "医師の知見を活かして選定"),
]

# 認証カテゴリ名としての「美白」「シワ改善」を保護するための判定キーワード
CERT_CONTEXT_KEYWORDS = ["認証", "機能性化粧品", "3機能性", "二重機能性", "機能性"]

def is_cert_context(text, pos, window=40):
    """指定位置の前後window文字以内に認証関連キーワードがあるか"""
    start = max(0, pos - window)
    end = min(len(text), pos + window)
    surrounding = text[start:end]
    return any(kw in surrounding for kw in CERT_CONTEXT_KEYWORDS)


def replace_protected(text, target, replacement):
    """target が認証カテゴリ文脈なら保護してスキップ、そうでなければ置換"""
    result = []
    last = 0
    for m in re.finditer(re.escape(target), text):
        start, end = m.span()
        if is_cert_context(text, start):
            continue  # 保護：置換しない
        result.append(text[last:start])
        result.append(replacement)
        last = end
    result.append(text[last:])
    return ''.join(result)


def process_file(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    original = text

    for target, repl in REPLACEMENTS:
        text = replace_protected(text, target, repl)

    # 美白 / シワ改善 単体は認証文脈以外を置換
    text = replace_protected(text, "美白", "透明感のある肌印象")
    text = replace_protected(text, "シワ改善", "乾燥による小じわを目立ちにくくするケア")

    if text != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    return False


targets = []
for pattern in ['index.html', 'ingredients/*.html', 'products/*.html', 'blog/*.html', 'doctor/*.html']:
    targets.extend(glob.glob(pattern))

print('=== 薬機法リスク表現置換 ===')
changed_files = []
for path in sorted(set(targets)):
    if process_file(path):
        changed_files.append(path)
        print(f'  Updated: {path}')

print(f'\n変更ファイル数: {len(changed_files)}')

# 検証：残存リスク表現の確認
print('\n=== 残存チェック（認証文脈以外）===')
RISKY = ["美白の王様", "最強の抗酸化成分", "シミ改善", "肌再生", "リフティング効果",
         "メラニン生成を抑制し", "角層の奥まで浸透", "深いうるおい", "医師監修", "医師推薦"]
for path in sorted(set(targets)):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    for r in RISKY:
        if r in text:
            print(f'  残存あり: {path} -> {r}')

print('\n=== 完了 ===')
