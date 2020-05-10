# videoDrive

<b>Initial Setup</b>

<ul>
 <li> `python3 -m venv ~/bvenv`
 <li> Activate Virtual Env
 <li> `pip install -r requirements.txt`
 <li> Run `python manage.py migrate`
</ul>

<b>Adding credentials</b>
<ul>
 <li> Run `python manage.py createsuperuser`
 <li> Enter a username and password
 <li> Run `python manage.py runserver` and login to `localhost:8080` using the above credentials
 <li> Enter the following credentials in `/admin/utils/setting/`:
 <ol>
    <li>Key:`CRON_FETCH_VIDEO_KEYWORDS`, Value:`football,cricket,official`
 </ol>
 <li> Enter the following credentials in `/admin/integrations_youtube/youtubecredentials/`:
 <ol>
    <li>name:[Any Name], ApiKey: API Key from <a href='https://console.developers.google.com/apis/credentials'>Console Page</a>, isActive=True
    <br>
    Note: Make sure you set the is_active field=True, otherwise that credentials will not be picked.  
 </ol>
</ul>


<b>Launch</b>


<ul>
 <li> Run `python manage.py crontab add`
 <li> Run `python manage.py runserver localhost:8000`
</ul>


<b>Run</b>


<ul>
 <li> After launch go to `http://localhost:8000/videos/`, to check the paginated API response for the list of stored viedeo details.
 <li> After launch go to `http://localhost:8000/videos/search/?q=[keywords]`, to check the paginated API response for search API. Eg: `http://localhost:8000/videos/search/?q=office,football,work`
</ul>


<b>Note</b>


<ul>
 <li> Add more Credentials in `YoutubeCredentials` model as it will automatically be picked next when one of them expires.
</ul>

