"""
Geocoder class
"""
###############################################################################
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
###############################################################################

import csv
import urllib2
import json


class Geocoder:
    def __init__(self, service=None):
        if service:
            self.process = service

    def process(self, inFile, outFile ):
        # explicitly set it up so this can't be called directly
        raise NotImplementedError('Exception raised, process is supposed to be an abstract class!')


# Geocode with Google Web Service
def processGoogle( inCSV, outCSV ):
    # read CSV file to information list
    print('Google geocode ...')
    with open(inCSV, 'rb') as f:
        reader = csv.reader(f)
        info_list = list(reader)
        
    # read address from information list, encode UTF-8, then geocode by Google Web Service
    for i in range(1,len(info_list)):
        address = info_list[i][1]
        addres_quote = urllib2.quote(address.decode('iso-8859-1').encode('utf8'))
        geocode_url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % addres_quote
        req = urllib2.urlopen(geocode_url)
        jsonResponse = json.loads(req.read())
        try: 
            info_list[i][2] = jsonResponse["results"][0]["geometry"]["location"]["lng"]
        except: 
            info_list[i][2] = "Not Found"
            pass
        try: 
            info_list[i][3] = jsonResponse["results"][0]["geometry"]["location"]["lat"] 
        except:
            info_list[i][3] = "Not Found"
            pass
    outFile = open(outCSV,'wb')
    wr = csv.writer(outFile, dialect='excel')
    wr.writerows(info_list)
    print('   done\n')


#Geocode with OpenStreetMap Web Service
def processOSM( inCSV, outCSV ):
    print('OSM geocode ...')
    with open(inCSV, 'rb') as f:
        reader = csv.reader(f)
        info_list = list(reader)

    # read address from information list, encode UTF-8, then geocode by Nominatim Open Street Map Web Service
    for i in range(1,len(info_list)):
        address = info_list[i][1]
        addres_quote = urllib2.quote(address.decode('iso-8859-1').encode('utf8'))
        geocode_url = "http://nominatim.openstreetmap.org/?format=json&addressdetails=1&q=%s&format=json&limit=1" % addres_quote
        req = urllib2.urlopen(geocode_url)
        jsonResponse = json.loads(req.read())
        try: 
            info_list[i][2] = jsonResponse[0]["lon"]
        except: 
            info_list[i][2] = "Not Found"
            pass

        try: 
            info_list[i][3] = jsonResponse[0]["lat"] 
        except:
            info_list[i][3] = "Not Found"
            pass


    outFile = open(outCSV,'wb')
    wr = csv.writer(outFile, dialect='excel')
    wr.writerows(info_list)
    print(' done\n')



if __name__ == "__main__":

    googleGeocoder = Geocoder(processGoogle)
    googleGeocoder.process('example.csv','example_google_geocoding.csv')
    
    osmGeocoder = Geocoder(processOSM)
    osmGeocoder.process('example.csv','example_osm_geocoding.csv')