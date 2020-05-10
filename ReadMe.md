# videoDrive

<b>Initial Setup</b>

 -`python3 -m venv ~/bvenv`
 - Activate Virtual Env
 - `pip install -r requirements.txt`
 - Run `python manage.py migrate`

<b>Adding credentials</b>

 - Run `python manage.py createsuperuser`
 - Enter a username and password
 - Run `python manage.py runserver` and login to `localhost:8080` using the above credentials
 - Enter the following credentials in `/admin/utils/setting/`:
    - Key:`CRON_FETCH_VIDEO_KEYWORDS`, Value:`football,cricket,official`
 - Enter the following credentials in `/admin/integrations_youtube/youtubecredentials/`:
    
    - name:[Any Name], ApiKey: API Key from <a href='https://console.developers.google.com/apis/credentials'>Console Page</a>, isActive=True
 
    Note: Make sure you set the is_active field=True, otherwise that credentials will not be picked.  


<b>Launch</b>

 - Run `python manage.py crontab add`
 - Run `python manage.py runserver localhost:8000`


<b>Run</b>

 - After launch go to `http://localhost:8000/videos/`, to check the paginated API response for the list of stored viedeo details.
 - After launch go to `http://localhost:8000/videos/search/?q=[keywords]`, to check the paginated API response for search API. Eg: `http://localhost:8000/videos/search/?q=office,football,work`


<b>Important Note</b>
 - Add more Credentials in `YoutubeCredentials` model as it will automatically be picked next when one of them expires.

