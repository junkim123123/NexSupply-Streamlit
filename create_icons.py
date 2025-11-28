"""
아이콘 생성 스크립트 (선택사항)
PWA용 아이콘 파일을 생성합니다.

사용법:
    python create_icons.py

주의: Pillow 라이브러리가 필요합니다.
    pip install Pillow
"""
try:
    from PIL import Image, ImageDraw, ImageFont
    import os
except ImportError:
    print("Pillow가 설치되지 않았습니다. 다음 명령어로 설치하세요:")
    print("pip install Pillow")
    exit(1)


def create_icon(size, filename, color="#0EA5E9"):
    """기본 아이콘 생성 (NexSupply 로고 대신 색상 배경 사용)"""
    # 이미지 생성
    img = Image.new('RGB', (size, size), color=color)
    draw = ImageDraw.Draw(img)
    
    # 중앙에 "N" 문자 추가 (간단한 로고 대체)
    try:
        # 시스템 폰트 사용
        font_size = size // 3
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # 기본 폰트 사용
        font = ImageFont.load_default()
    
    # 텍스트 그리기
    text = "N"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size - text_width) // 2, (size - text_height) // 2)
    
    draw.text(position, text, fill="white", font=font)
    
    # 저장
    img.save(filename)
    print(f"✅ {filename} 생성 완료 ({size}x{size})")


def main():
    """메인 함수"""
    print("NexSupply PWA 아이콘 생성 중...")
    
    # static/icons 폴더 생성
    os.makedirs("static/icons", exist_ok=True)
    
    # 아이콘 생성 (static/icons/ 경로에)
    create_icon(192, "static/icons/icon-192.png")
    create_icon(512, "static/icons/icon-512.png")
    
    print("\n✅ 모든 아이콘 생성 완료!")
    print("\n다음 파일들이 생성되었습니다:")
    print("  - static/icons/icon-192.png")
    print("  - static/icons/icon-512.png")
    print("\n💡 실제 로고가 있다면 이 파일들을 교체하세요.")
    print("\n📝 manifest.json 경로: /app/static/icons/icon-192.png")


if __name__ == "__main__":
    main()

