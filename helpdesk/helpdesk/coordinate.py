'''
Google Coordinate Ticket Integration
'''
import httplib2
import settings
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from google.appengine.ext import db
from google.appengine.api import memcache


PROGRESS_CHOICES = {
    1:'NOT_STARTED',
    2:'IN_PROGRESS',
    3:'COMPLETED',
    4:'OBSOLETE',
    5:'OBSOLETE',
}

class Coordinate():
    def __init__(self):
        self.credentials = self.__auth__()
        http = httplib2.Http(cache=memcache)
        http = self.credentials.authorize(http)
        api = build("coordinate", "v1", http=http)
        self.client  = api.jobs()

    '''
       Handles requesting and storing Google OAuth2 credentials
    '''
    def __auth__(self):
        storage = Storage('%s/%s' % (settings.PROJECT_PATH,'googlecoordinate_oauth2.dat'))
        credentials = storage.get()
        if credentials is None or credentials.invalid == True:
            flow = OAuth2WebServerFlow(
                client_id     = settings.GOOGLE_COORDINATE_CLIENT_ID,
                client_secret = settings.GOOGLE_COORDINATE_CLIENT_SECRET,
                scope         = 'https://www.googleapis.com/auth/coordinate')
            credentials = run(flow,storage)
        return credentials

    '''
       Takes a ticket and inserts it
    '''
    def Insert(self,ticket):
        result = self.client.insert(body='',
                          title=ticket.title,
                          teamId=ticket.queue.coordinate_id,
                          address=ticket.location,
                          lat=ticket.lat,
                          lng=ticket.lon,
                          note=ticket.description,
                          ).execute()        
        return result

    '''
       Lists the jobs for a team
    '''
    def List(self,queue_id):
        flag = True
        results = {'items':[]}
        nextpagetoken = None
        while flag:
          result = None
          if nextpagetoken is not None:
            result = self.client.list(teamId=queue_id,pageToken=nextpagetoken).execute()
          else:
            result = self.client.list(teamId=queue_id).execute()

          if result.has_key('items'):
            flag = True
            results['items'] += result['items']
            nextpagetoken = result['nextPageToken']
          else:
            flag = False
        return results

    '''
       Updates the status of a ticket
    '''
    def Update(self,ticket):
        result = self.client.update(body="",
                                    teamId=ticket.queue.coordinate_id,
                                    jobId=ticket.coordinate_id,
                                    #address=ticket.location,
                                    #assignee=ticket.assigned_to,
                                    #lat=ticket.lat,
                                    #lng=ticket.lon,
                                    #title=ticket.title,
                                    progress=PROGRESS_CHOICES[ticket.status],
                                    ).execute()
        return result


    '''
       Closes a ticket.
    '''
    def Close(self,ticket):
        return  self.client.update(body="",
                                   teamId=ticket.queue.coordinate_id,
                                   jobId=ticket.coordinate_id,
                                   progress=PROGRESS_CHOICES[3],
                                   ).execute()
