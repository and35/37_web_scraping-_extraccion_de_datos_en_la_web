import scrapy
from scrapy.crawler import CrawlerProcess

# creamos una herencia del objeto scrapy spider
class Spider12(scrapy.Spider):
    name = 'spider12'
    # dominios a scrapear
    allowed_domains = ['pagina12.com.ar']
    # formato de archivo de salida
    custom_settings = {
    'FEEDS':
        {   "pagina12.json":
            {
                "format":"json",
                "encoding":"utf-8",
            }
        },
    "DEPTH_LIMIT":2
    }

    # URLS a scrapear. son todas las secciones del diario 
    starts_urls = [ 'https://www.pagina12.com.ar/secciones/el-pais',
                    'https://www.pagina12.com.ar/secciones/economia',
                    'https://www.pagina12.com.ar/secciones/sociedad',
                    'https://www.pagina12.com.ar/suplementos/cultura-y-espectaculos',
                    'https://www.pagina12.com.ar/secciones/el-mundo',
                    'https://www.pagina12.com.ar/secciones/deportes',
                    'https://www.pagina12.com.ar/secciones/contratapa',
                    'https://www.pagina12.com.ar/secciones/audiovisuales']
    print("000"*50)

    # creamos un metodo obtener los links a cada nota 
    def parse(self, response): # response es el equivalente de hacer un requests.get()
        # Listado de  links notas
        links_notas = response.xpath("//h4[@class='title-list']/a/@href").getall() # faltan h3,h2
        print(links_notas[0], "++++"*40)
        for nota in links_notas: 
            # canalizar la respuesta hacia el metodo parse_nota
            # yield == return, solo que direcciona el resultado a otro metodo
            # for url in articles_title:
            nota = 'https://www.pagina12.com.ar' + nota
            yield response.follow(nota, callback=self.parse_nota)
        # creamos accedemos al boton de siguiente pagina
        next_page = 'https://www.pagina12.com.ar{}'.format(response.xpath('//a[@class="next"]/@href').get())
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
    # creamos un metodo para analizar contenido de cada nota 
    def parse_nota(self, response):
        title = response.xpath('//h1/text()').get()
        summary = response.xpath('//h2/text()').get() 
        yield{"url": response.url,
                "titulo": title,
                "resumen": summary}
        

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(Spider12)
    process.start()