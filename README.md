
# VibeCheck

An application that generates a recommended playlist based on your "vibes". 


Built with  [Spotify API](https://developer.spotify.com/documentation/web-api/),
[Django](https://django.readthedocs.io/en/stable/),
[W3.CSS](https://www.w3schools.com/w3css/defaulT.asp),
[Django AllAuth](https://django-allauth.readthedocs.io/en/latest/)

 


## About 

Each vibe is associated with the following genres:
- Positive: pop, edm, indie-pop, happy, k-pop
- Chillax: r-n-b, indie, jazz, alternative, chill, soul
- Focus: study, electronic, classical, jazz
- Hype: edm, rock, hip-hop, dance, pop


Based on the user's selected vibe, seed data is selected from a random combination of associated genres and user's liked songs. This seed data is used to create [recommendations](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-recommendations). 


## Demo


https://user-images.githubusercontent.com/64836972/207677125-12911bea-1a4d-41a3-8fc0-37995bd31ed5.mp4

