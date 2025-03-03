import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import re

# Definir un User-Agent realista para evitar bloqueos
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_sitemap_urls(sitemap_url):
    """Obtiene todas las URLs dentro de un sitemap XML."""
    try:
        response = requests.get(sitemap_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'lxml-xml')
        return [loc.text for loc in soup.find_all('loc')]
    except Exception as e:
        print(f"⚠ Error obteniendo sitemap {sitemap_url}: {e}")
        return []

def get_image_urls(page_url):
    """Extrae imágenes PNG y JPG, incluyendo las cargadas con lazy-loading."""
    try:
        response = requests.get(page_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        images = set()

        # Extraer imágenes de tags <img>
        for img in soup.find_all('img'):
            # Buscar en múltiples atributos donde pueden estar URLs de imágenes
            for attr in ['src', 'data-src', 'data-original', 'data-srcset', 'data-lazy-src']:
                img_url = img.get(attr)
                if img_url:
                    # Si es data-srcset, tomar la primera URL
                    if ' ' in img_url:
                        img_url = img_url.split()[0]
                    img_url = urljoin(page_url, img_url)
                    if img_url.lower().endswith(('.png', '.jpg', '.jpeg')):
                        images.add((img_url, page_url))
                        print(f"  - Imagen encontrada (img tag): {img_url}")

        # Extraer imágenes de galerías/lightbox
        # Buscar tanto .lbox-trigger-item como cualquier clase que contenga lbox-trigger
        for a in soup.find_all('a'):
            # Verificar si el enlace tiene cualquier clase relacionada con lightbox
            if a.get('class') and any('lbox-trigger' in cls for cls in a.get('class')):
                img_url = a.get('href')
                if img_url and img_url.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img_url = urljoin(page_url, img_url)
                    images.add((img_url, page_url))
                    print(f"  - Imagen encontrada (lightbox): {img_url}")
            
            # También verificar cualquier enlace que apunte a imágenes directamente
            elif a.get('href') and a.get('href').lower().endswith(('.png', '.jpg', '.jpeg')):
                img_url = urljoin(page_url, a.get('href'))
                images.add((img_url, page_url))
                print(f"  - Imagen encontrada (enlace directo): {img_url}")

        # Buscar patrones adicionales específicos para esta web
        # Buscar en atributos data-* que puedan contener URLs de imágenes
        for element in soup.find_all(attrs={"data-lg-size": True}):
            img_url = element.get('href')
            if img_url and img_url.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_url = urljoin(page_url, img_url)
                images.add((img_url, page_url))
                print(f"  - Imagen encontrada (galería lightbox): {img_url}")

        # Buscar URLs de imágenes en atributos style (fondos)
        for element in soup.find_all(lambda tag: tag.get('style') and 'background' in tag.get('style', '')):
            style = element.get('style')
            urls = re.findall(r'url\([\'"]?(.*?)[\'"]?\)', style)
            for url in urls:
                if url.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img_url = urljoin(page_url, url)
                    images.add((img_url, page_url))
                    print(f"  - Imagen encontrada (background): {img_url}")

        return list(images)
    except Exception as e:
        print(f"⚠ Error obteniendo imágenes de {page_url}: {e}")
        return []

def process_sitemap(sitemap_url, depth=0):
    """Procesa un sitemap y extrae imágenes de cada página listada."""
    print(f"📂 Procesando sitemap (nivel {depth}): {sitemap_url}")
    urls = get_sitemap_urls(sitemap_url)
    all_images = []

    for url in urls:
        if url.endswith('.xml'):
            all_images.extend(process_sitemap(url, depth + 1))  # Procesar sub-sitemaps
        else:
            images = get_image_urls(url)
            print(f"📸 {len(images)} imágenes encontradas en {url}")
            all_images.extend(images)

    return all_images

def main():
    sitemap_url = "https://idpc.gov.co/sanjuandedios/sitemap.xml"
    all_images = process_sitemap(sitemap_url)

    print(f"✅ Total de imágenes PNG/JPG encontradas: {len(all_images)}")

    if all_images:
        with open("images.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Image URL", "Page URL"])
            for img, page in all_images:
                writer.writerow([img, page])
        print("💾 Imágenes guardadas en images.csv")
    else:
        print("⚠ No se encontraron imágenes PNG/JPG para guardar.")

if __name__ == "__main__":
    main()