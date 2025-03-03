# Extracción y Filtrado de Imágenes desde un Sitio Web

Este programa permite obtener imágenes desde un sitio web de manera automática, utilizando un archivo especial llamado "sitemap". Además, filtra y guarda las imágenes en un archivo CSV, eliminando aquellas que contienen logotipos o imágenes duplicadas. Posteriormente, el resultado se organiza en una galería visual donde cada imagen tiene un enlace directo a la página de origen.

El proceso comienza accediendo al sitio web de manera segura, simulando ser un navegador real para evitar bloqueos. Luego, se extraen todas las direcciones de páginas web listadas en un archivo sitemap. Si dentro del sitemap se encuentran otros sitemaps adicionales, estos también son procesados. Una vez obtenidas las URLs de todas las páginas, el programa busca imágenes dentro de cada una de ellas, examinando etiquetas visibles y enlaces ocultos.

Después de identificar las imágenes, se filtran aquellas que corresponden a logotipos o archivos específicos no deseados. También se evita la duplicación de imágenes, garantizando que solo se conserven archivos únicos. Finalmente, la lista de imágenes seleccionadas se guarda en un archivo CSV llamado **images.csv** y se dispone en una galería visual, donde cada imagen se muestra junto con su enlace original, permitiendo acceder fácilmente a la página de donde proviene.

No se requieren conocimientos técnicos para utilizar este programa. Una vez ejecutado, generará automáticamente un archivo CSV con las imágenes extraídas y una galería con los enlaces a sus páginas de origen, facilitando la navegación y consulta de los resultados.

**Nota:** Este programa está diseñado para fines educativos y de investigación. Se recomienda respetar los derechos de autor y la propiedad intelectual al utilizarlo. Se creó para la revisión de material audiovisual disponible en el [IDPC](https://idpc.gov.co/) sobre el  Hospital San Juan de Dios, ocasionalmente es un script que podría funcionar en otro sitio web que contenga archivos de mapas de sitio ``sitemap.xml``.

