herbalcell
---------

Source code for Django based website [herbalcell.com](http://herbalcell.com).


About
-----

I've been using my personal website as a way to learn web programming for years since my humble beginnings getting my feet wet learning html.

Most recently I've been working on adjusting my CSS to be responsive for mobile and tablets.

I wrote a custom blog app in Django, and recently updated it for Django 1.5. I designed it to be easily updatable when I add various new things to my site. I simply run my rsync script to upload any new content, and then run an update management command.

Makes use of caching, Google Analytics api, custom templatetags, logging, custom context processor, and feed. Saves models to the database to keep track of objects created when updating. Also uses mutagen for reading ID3 tags, PIL for creating thumbnails and runs external processes like zip/unzip.

Custom Jquery to keep ads at the top of the page when scrolling, and to show/hide sidebar of articles sorted by date/popularity. Also incorporated Jquery apps like Fancybox, BeforeAfter, Smooth Div Scroll (photo gallery), 360 Audio Player.

Designed all HTML templates and generated CSS using Less. I use custom embedded fonts, media queries, Less Elements, Jquery Migrate, and respond.js.