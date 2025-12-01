import streamlit as st
import os
import io
import zipfile
import requests
from PIL import Image
import fal_client
import time

# ---------------------------------------------------------
# 設定
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="🎬 Nanobanana Pro 3x3 シーンカット")
st.title("🎬 Nanobanana Pro: 3x3 シーンカット生成")
st.caption("1枚の写真から映画のような9種類のカットを自動生成します (Nanobanana Pro使用)")

# サイドバー
with st.sidebar:
    st.header("⚙️ 設定")
    fal_key = st.text_input("fal API Key (必須)", type="password", help="fal.aiのAPIキーを入力してください")
    if fal_key:
        os.environ["FAL_KEY"] = fal_key
    
    st.divider()
    st.subheader("📝 生成パラメータ")
    resolution = st.selectbox(
        "解像度",
        ["1K", "4K"],
        index=0,
        help="1K: 標準（速い、$0.15）/ 4K: 高解像度（遅い、$0.30）"
    )
    aspect_ratio = st.selectbox(
        "アスペクト比",
        ["auto", "16:9", "1:1", "4:3", "3:4", "9:16"],
        index=1,
        help="生成される画像のアスペクト比（autoは元画像に合わせます）"
    )
    
    st.divider()
    st.markdown("### 📖 使い方")
    st.markdown("""
    1. fal API Keyを入力
    2. 画像をアップロード
    3. 「生成開始」をクリック
    4. 気に入ったカットを選択
    5. ZIPでダウンロード
    """)

# ---------------------------------------------------------
# プロンプト（Nanobananaメソッド）
# ---------------------------------------------------------
NANOBANANA_EXACT_PROMPT = """<instruction>
Analyze the entire composition of the input image. Identify ALL key subjects present (whether it's a single person, a group/couple, a vehicle, or a specific object) and their spatial relationship/interaction.
Generate a cohesive 3x3 grid "Cinematic Contact Sheet" featuring 9 distinct camera shots of exactly these subjects in the same environment.
You must adapt the standard cinematic shot types to fit the content (e.g., if a group, keep the group together; if an object, frame the whole object):

**Row 1 (Establishing Context):**
1. **Extreme Long Shot (ELS):** The subject(s) are seen small within the vast environment.
2. **Long Shot (LS):** The complete subject(s) or group is visible from top to bottom (head to toe / wheels to roof).
3. **Medium Long Shot (American/3-4):** Framed from knees up (for people) or a 3/4 view (for objects).

**Row 2 (The Core Coverage):**
4. **Medium Shot (MS):** Framed from the waist up (or the central core of the object). Focus on interaction/action.
5. **Medium Close-Up (MCU):** Framed from chest up. Intimate framing of the main subject(s).
6. **Close-Up (CU):** Tight framing on the face(s) or the "front" of the object.

**Row 3 (Details & Angles):**
7. **Extreme Close-Up (ECU):** Macro detail focusing intensely on a key feature (eyes, hands, logo, texture).
8. **Low Angle Shot (Worm's Eye):** Looking up at the subject(s) from the ground (imposing/heroic).
9. **High Angle Shot (Bird's Eye):** Looking down on the subject(s) from above.

Ensure strict consistency: The same people/objects, same clothes, and same lighting across all 9 panels. The depth of field should shift realistically (bokeh in close-ups).
</instruction>

A professional 3x3 cinematic storyboard grid containing 9 panels.
The grid showcases the specific subjects/scene from the input image in a comprehensive range of focal lengths.
**Top Row:** Wide environmental shot, Full view, 3/4 cut.
**Middle Row:** Waist-up view, Chest-up view, Face/Front close-up.
**Bottom Row:** Macro detail, Low Angle, High Angle.
All frames feature photorealistic textures, consistent cinematic color grading, and correct framing for the specific number of subjects or objects analyzed."""

# カット名の定義
CUT_NAMES = [
    "1. 超広角ショット (ELS)",
    "2. ロングショット (LS)", 
    "3. ミディアムロング (3/4)",
    "4. ミディアムショット (MS)",
    "5. ミディアムクローズアップ (MCU)",
    "6. クローズアップ (CU)",
    "7. 超クローズアップ (ECU)",
    "8. ローアングル (虫の視点)",
    "9. ハイアングル (鳥の視点)"
]

# ---------------------------------------------------------
# セッション状態の初期化
# ---------------------------------------------------------
if 'generated_grid' not in st.session_state:
    st.session_state.generated_grid = None
if 'grid_crops' not in st.session_state:
    st.session_state.grid_crops = []
if 'original_image' not in st.session_state:
    st.session_state.original_image = None

# ---------------------------------------------------------
# メイン処理
# ---------------------------------------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 画像アップロード")
    uploaded_file = st.file_uploader("写真を選択してください", type=["jpg", "png", "jpeg", "webp"])
    
    if uploaded_file:
        # 元画像を保存して表示
        st.session_state.original_image = Image.open(uploaded_file)
        st.image(st.session_state.original_image, caption="アップロードされた画像", use_container_width=True)

with col2:
    st.subheader("🎬 生成設定")
    if uploaded_file:
        st.success("✅ 画像が読み込まれました")
        if st.button("🚀 3x3シーンカット生成開始", type="primary", use_container_width=True):
            if not os.environ.get("FAL_KEY"):
                st.error("⚠️ サイドバーでfal API Keyを入力してください")
            else:
                progress_bar = st.progress(0)
                status = st.empty()
                
                try:
                    # ステップ1: 画像アップロード
                    status.info("📤 画像をアップロード中...")
                    progress_bar.progress(10)
                    uploaded_file.seek(0)  # ファイルポインタをリセット
                    img_bytes = uploaded_file.getvalue()
                    img_url = fal_client.upload(img_bytes, "image/png")
                    
                    # ステップ2: AI生成開始
                    status.info("🎨 Nanobanana Pro で3×3グリッド生成中... (品質優先のため1-2分程度かかります)")
                    progress_bar.progress(30)
                    
                    result = fal_client.subscribe(
                        "fal-ai/nano-banana-pro/edit",
                        arguments={
                            "prompt": NANOBANANA_EXACT_PROMPT,
                            "image_urls": [img_url],  # リスト形式で渡す
                            "num_images": 1,
                            "aspect_ratio": aspect_ratio,
                            "output_format": "png",
                            "resolution": resolution
                        }
                    )
                    
                    progress_bar.progress(70)
                    
                    # ステップ3: 画像取得
                    status.info("📥 生成画像を取得中...")
                    gen_url = result["images"][0]["url"]
                    response = requests.get(gen_url)
                    gen_img = Image.open(io.BytesIO(response.content))
                    
                    st.session_state.generated_grid = gen_img
                    progress_bar.progress(85)
                    
                    # ステップ4: 9分割処理
                    status.info("✂️ 9分割処理中...")
                    w, h = gen_img.size
                    crops = []
                    for i in range(3):
                        for j in range(3):
                            box = (j*(w//3), i*(h//3), (j+1)*(w//3), (i+1)*(h//3))
                            crops.append(gen_img.crop(box))
                    st.session_state.grid_crops = crops
                    
                    progress_bar.progress(100)
                    status.success("✅ 生成完了！下にスクロールして結果を確認してください")
                    time.sleep(1)
                    st.rerun()
                    
                except Exception as e:
                    status.error(f"❌ エラーが発生しました: {str(e)}")
                    progress_bar.empty()
    else:
        st.info("👆 左側で画像をアップロードしてください")

# ---------------------------------------------------------
# 結果表示とダウンロード
# ---------------------------------------------------------
if st.session_state.generated_grid:
    st.write("---")
    st.header("🎬 生成結果")
    
    # 生成されたグリッド全体を表示
    st.subheader("📊 3x3グリッド全体")
    st.image(st.session_state.generated_grid, use_container_width=True, caption="生成された3x3シーンカットグリッド")
    
    # 個別カット選択
    st.write("---")
    st.subheader("✂️ 個別カット選択")
    st.caption("ダウンロードしたいカットをチェックしてください")
    
    selected = []
    
    # 3x3のグリッドで表示
    for row in range(3):
        cols = st.columns(3)
        for col_idx in range(3):
            i = row * 3 + col_idx
            with cols[col_idx]:
                st.image(st.session_state.grid_crops[i], use_container_width=True)
                if st.checkbox(CUT_NAMES[i], key=f"cut_{i}"):
                    selected.append(i)
    
    # ダウンロードセクション
    if selected:
        st.write("---")
        st.subheader(f"💾 ダウンロード ({len(selected)}個選択中)")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            upscale_mode = st.radio(
                "品質オプション",
                ["そのまま保存（高速）", "高画質化して保存（約2倍解像度、時間かかります）"],
                help="高画質化は選択したカット1枚あたり10-20秒程度かかります"
            )
        
        with col2:
            if st.button("📦 ZIP作成＆ダウンロード", type="primary", use_container_width=True):
                download_progress = st.progress(0)
                download_status = st.empty()
                
                try:
                    buf = io.BytesIO()
                    with zipfile.ZipFile(buf, "w") as z:
                        total = len(selected)
                        for idx, i in enumerate(selected):
                            download_status.info(f"処理中... ({idx+1}/{total})")
                            download_progress.progress((idx) / total)
                            
                            img = st.session_state.grid_crops[i]
                            out = io.BytesIO()
                            img.save(out, "PNG")
                            
                            # 高画質化処理
                            if "高画質化" in upscale_mode and os.environ.get("FAL_KEY"):
                                try:
                                    out.seek(0)
                                    u_url = fal_client.upload(out.getvalue(), "image/png")
                                    upscale_result = fal_client.subscribe(
                                        "fal-ai/ccsr",
                                        arguments={
                                            "image_url": u_url,
                                            "scale": 2
                                        }
                                    )
                                    final_data = requests.get(upscale_result["image"]["url"]).content
                                    z.writestr(f"cut_{i+1:02d}_{CUT_NAMES[i].split('.')[1].strip()}_upscaled.png", final_data)
                                except Exception as e:
                                    download_status.warning(f"カット{i+1}の高画質化に失敗。元画質で保存します。")
                                    out.seek(0)
                                    z.writestr(f"cut_{i+1:02d}_{CUT_NAMES[i].split('.')[1].strip()}.png", out.getvalue())
                            else:
                                z.writestr(f"cut_{i+1:02d}_{CUT_NAMES[i].split('.')[1].strip()}.png", out.getvalue())
                        
                        download_progress.progress(1.0)
                    
                    download_status.success("✅ ZIP作成完了！")
                    
                    # ダウンロードボタン
                    st.download_button(
                        label="⬇️ ZIPファイルをダウンロード",
                        data=buf.getvalue(),
                        file_name=f"nanobanana_cuts_{len(selected)}files.zip",
                        mime="application/zip",
                        use_container_width=True
                    )
                    
                except Exception as e:
                    download_status.error(f"❌ ZIP作成エラー: {str(e)}")
    else:
        st.info("💡 ダウンロードしたいカットにチェックを入れてください")

# フッター
st.write("---")
st.caption("Powered by fal.ai Nanobanana Pro | 3×3 Cinematic Contact Sheet Generator")
