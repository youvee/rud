# rud
---

##Usage
    ./rud.py username1 username2 username3 username4 ...

##Introduction
Reddit URL Downloader.  Downloads all supported files that are on a user's /submitted page.

###Supported Sites
- [Gfycat](http://gfycat.com/)
- [Imgur](http://imgur.com/)
- [Vidble](http://vidble.com/)
- [vidme](https://vid.me/)

##Requirements
**Python**.  No modules not included in the Python standard libraries were used.

##Issues
I have not done testing beyond my personal use of the program.  The program has worked for my personal use, but there are undoubtedly aspects of the various sites this program operates on that can break it.

###Known issue
When downloading content from Vidble, requests start timing out, and you won't be able to access vidble.com for around 5 minutes or so.  I'm unsure if this is due to overzealous rate-limiting, but it's impossible to get around since Vidble doesn't have a public API, and they don't mention their policies on requests anywhere.

###Reporting issues
Please report all feedback or bugs on the [GitHub issues page](https://github.com/Manic0892/rud/issues).

##Contributions
Contributions are welcome--shoot me a pull request.  The code is messy, the result of working on it infrequently over a large span of time.  I'm hoping to clean it up and document it properly in the future.  If you want to add functionality or fix bugs despite this, I'd be more than happy to work with you.

##Contact
If you don't want to contact me through the GitHub issues page, you can message me [on Reddit](https://www.reddit.com/message/compose/?to=Manic0892).