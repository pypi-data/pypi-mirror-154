from scraper import *


class Download:
    def __init__(self,url):
        self.url = url
        self.Scpr = Scpr
    def download(self):
        links = self.Scpr.get_info(self)
        for lnk in links:
            lnk_splt = lnk.split("/")
            with open("arXiv."+str(lnk_splt[4]+".pdf"),"wb") as f:
                print("\nDownloading ...")
                dwn = requests.get(lnk,stream=True)
                size = dwn.headers.get("content-length")
                size = int(size)
                ch_size = int(size/50)
                stp = 0
                for data in dwn.iter_content(chunk_size=ch_size):
                    print("\r{}MB [{}{}] {}%".format(round(stp*ch_size/1e6,2),"="*stp," "*(50 - stp),round(stp*ch_size*100/size,2)),end="")
                    f.write(data)
                    stp += 1


class newDonwload():
    from pyodide.http import pyfetch
    import pandas as pd

    async def download(url,filename):
        response = await pyfetch(url)
        if response.status == 200:
            with open(filename,"wb") as f:
                f.write(await response.bytes())

await newDonwload(filename,"Example1.txt")