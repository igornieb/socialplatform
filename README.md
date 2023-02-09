# socialplatform
## 1. Descryption
social platform made using Django with REST API and Bootstrap frontend.

social platform is a photo social service. It lets you host your own pictures, follow other users and like their posts.
![image](https://user-images.githubusercontent.com/66256669/217853218-d5275c6e-ddc5-4cc0-b800-b8c6705eda97.png)

# Table of Contents
1. [Descryption](#1-Descryption)
1. [Live website](#2-live-website)
3. [Api endpoints](#3-api-endpoints)
   1. [/api/posts/](#apiposts)
   2. [/api/user/{id}](#apiuserid)
   3. [/api/user/follows/{id}](#apiuserfollowsid)
   4. [/api/user/followers/{id}/](#apiuserfollowersid)
   5. [/api/settings](#apisettings)
   6. [/api/follow/{id}](#apifollowid)
   7. [/api/post/{id}](#apipostid)
   8. [/api/post/comments/{id}](#apipostcommentsid)
   9. [/api/comment/{id}](#apicommentid)
   10. [/api/post/likes/{id}](#apipostlikesid)
   11. [/api/trending/post/{days}](#apitrendingpostdays)
   12. [/api/trending/users](#apitrendingusers)
   13. [/api/search/{query}](#apisearchquery)
   14. [/api/notifications](#apinotifications)
   15. [/api/register](#apiregister)
   16. [login/authentication](#loginauthentication)
## 2. Live Website
LINK
## 3. API endpoints
### /api/posts/
  #### GET
   Returns list of posts from people you follow.
   
   Succes: 201
   
   Example:
   
          ```[
                {
                  "pk": 1,
                  "owner": {
                    "pk": 1,
                    "username": "admin",
                    "profile_picture": "/media/media/user_1/profile/cattt605281251_U5Yl9sR.jpg",
                    "name": "Admin AGH",
                    "bio": "Im admin of this platform",
                    "followers": 0,
                    "follows": 2
                  },
                  "description": "My new kaczkaa",
                  "picture": "/media/media/user_1/posts/kaczk.jpg",
                  "date": "2022-11-16T21:53:18Z",
                  "no_of_likes": 0
                }
                ...
             ]```
  #### POST
   Allows user that is signed in to add new post.
   
   Succes code: 201
   
   Error code: 403
   
   Example:
   
        ```{
             "description": "My new kaczkaa",
             "picture": "/media/media/user_1/posts/kaczk.jpg"
            }```
   
### /api/user/{id}
  #### GET
   Returns profile of user with given id.
   
   Succes code: ```200```
   
   Error code: 
   
```404``` - not found
   
   Example:
   
        {
            "pk": 1,
            "username": "admin",
            "profile_picture": "/media/media/user_1/profile/cattt605281251_U5Yl9sR.jpg",
            "name": "Admin AGH",
            "bio": "Im admin of this platform",
            "followers": 0,
            "follows": 2
         }
### /api/user/follows/{id}
  #### GET
   Returns list of users that user with a given id follows.
   
   Succes code: ```200```
   
   Error code: 

   ```404``` - user not found
   
   Example:
   
        [
          {
              "follower": "admin",
              "follower_url": "/user/1",
              "followed": "igorniebylski",
              "followed_url": "/user/14"
          },
          ...
        ]
### /api/user/followers/{id}
  #### GET
   Returns list of users that are followin user with a given id.
   
   Succes code: ```200```
   
   Error code: 
   ```404``` - not found
   
   Example:
   
        [
          {
              "follower": "admin",
              "follower_url": "/user/1",
              "followed": "igorniebylski",
              "followed_url": "/user/14"
          },
          ...
        ]
### /api/settings
  #### GET
   Lets logged in user view their account info.
   
   Succes code: ```200```
   
   Error code: 
   
```403``` - access denied
   
   Example:
   
        {
          "pk": 1,
          "username": "admin",
          "profile_picture": "/media/media/user_1/profile/cattt605281251_U5Yl9sR.jpg",
          "name": "Admin",
          "bio": "Im admin of this platform",
          "followers": 0,
          "follows": 2
        }
  #### PATCH
   Lets user update their account info.
   
   Success code: ```200```
   
   Error code:
   
   ```403``` - user is not authenticated
   
   ```400``` - wrong input
   
   Example:
   
      ```{
          "profile_picture": "/media/media/user_1/profile/cattt605281251_U5Yl9sR.jpg",
          "name": "Admin",
          "bio": "Im admin of this platform",
         }```
### /api/follow/{id}
  #### GET
   Follows/unfollows user with a given id
   
   Succes code: 200, 201
   
   Error code: 
   
```404``` user not found
    
```403``` user is not authenticated
   
```400``` other error
   
 ### /api/post/{id}
  #### GET
   Gets post with given id.
   
   Succes code: ```200```
   
   Error code: 
   
```404``` post not found
    
```403``` user is not authenticated
   
```400``` bad request
   
   Example:
   
     {
      "post_url": "/post/1",
      "owner": {
          "pk": 1,
          "username": "admin",
          "profile_picture": "/media/media/user_1/profile/cattt605281251_U5Yl9sR.jpg",
          "name": "Admin AGH",
          "bio": "Im admin of this platform",
          "followers": 0,
          "follows": 2
      },
      "picture": "/media/media/user_1/posts/kaczk.jpg",
      "description": "My new kaczkaa",
      "date": "2022-11-16T21:53:18Z",
      "no_of_likes": 0
    }
  
  #### PATCH
   Lets owner edit their post description.
   
   Success code: ```200```
   
   Error code: 
   
```404``` post not found
    
```403``` user is not authenticated
   
```400``` bad request
   
   Example:
   
     {
      "description": "My new kaczkaa"
     }
  #### DELETE
   Deletes post with given id.
   
   Success code: ```204```
   
   Error code: 
   
```404``` post not found
    
```403``` user is not authenticated
   
### /api/post/comments/{id}
  #### GET
   Get comments related to post with given id.
   
   Success code: ```200```
   
   Error code: 
   
```404``` post not found
         
   Example:
   
     [
      {
        "comment_pk": 45,
        "owner": {
            "pk": 1,
            "username": "admin",
            "profile_picture": "/media/media/user_1/profile/cattt605281251_U5Yl9sR.jpg",
            "name": "Admin AGH",
            "bio": "Im admin of this platform",
            "followers": 0,
            "follows": 2
        },
        "post": {
            "pk": 1,
            "owner": {
                "pk": 1,
                "username": "admin",
                "profile_picture": "/media/media/user_1/profile/cattt605281251_U5Yl9sR.jpg",
                "name": "Admin AGH",
                "bio": "Im admin of this platform",
                "followers": 0,
                "follows": 2
            },
            "description": "My new kaczkaa",
            "picture": "/media/media/user_1/posts/kaczk.jpg",
            "date": "2022-11-16T21:53:18Z",
            "no_of_likes": 0
        },
        "comment": "TEST2",
        "date": "2022-12-06T20:04:37.069064Z"
    },
    ...
    ]
  
  #### POST
   Adds comment to post with given id.
   
   Succes code: 201
   
   Error code: 
   
    ```404``` post not found
    
   ```403``` user is not authenticated
   
   ```400``` bad request
   
   Example:
   
     ```{
      "comment": "new comment"
    }```
### /api/comment/{id}
####GET
Gets comment with given id.
      
Succes code: ```200```
      
Error code:
      
```404``` comment not found
      
Example:

    {
        "comment_pk": 45,
        "owner": {
            "pk": 1,
            "username": "admin",
            "profile_picture": "/media/media/user_1/profile/cattt605281251_U5Yl9sR.jpg",
            "name": "Admin AGH",
            "bio": "Im admin of this platform",
            "followers": 0,
            "follows": 2
        },
        "post": {
            "pk": 1,
            "owner": {
                "pk": 1,
                "username": "admin",
                "profile_picture": "/media/media/user_1/profile/cattt605281251_U5Yl9sR.jpg",
                "name": "Admin AGH",
                "bio": "Im admin of this platform",
                "followers": 0,
                "follows": 2
            },
            "description": "My new kaczkaa",
            "picture": "/media/media/user_1/posts/kaczk.jpg",
            "date": "2022-11-16T21:53:18Z",
            "no_of_likes": 0
        },
        "comment": "TEST2",
        "date": "2022-12-06T20:04:37.069064Z"
        }
    
#### PATCH
Lets owner edit comment with given id.
  
Success code: ```200```
      
Error code:
      
```404``` comment not found
```403``` user is not authenticated
```400``` bad request
  
  Example:

  ```
  {
  'comment':'edit comment'
  }
  ```
  
  #### DELETE
  Deletes comment with given id.
  
  Success code: ```204```
            
  Error code:
  
  ```404``` comment not found

  ```403``` user is not authenticated
  
### /api/post/likes/{id}
#### GET
Returns list of users that liked post with given id.

Success code: ```200```

Error code:

```404``` - post not found

Example:

```
[
    {
        "user": {
            "pk": 1,
            "username": "admin",
            "profile_picture": "/media/media/user_1/profile/cattt605281251_U5Yl9sR.jpg",
            "name": "Admin AGH",
            "bio": "Im admin of this platform",
            "followers": 0,
            "follows": 2
        },
        "post": {
            "post_url": "/post/1",
            "owner": {
                "pk": 1,
                "username": "admin",
                "profile_picture": "/media/media/user_1/profile/cattt605281251_U5Yl9sR.jpg",
                "name": "Admin AGH",
                "bio": "Im admin of this platform",
                "followers": 0,
                "follows": 2
            },
            "picture": "/media/media/user_1/posts/kaczk.jpg",
            "description": "My new kaczkaa",
            "date": "2022-11-16T21:53:18Z",
            "no_of_likes": 0
        }
    }
    ...
]
```
#### POST
Likes post with a given id.

Success code: ```200```

Error code:

```404``` - post not found

```403``` - user is not authenticated
  
### /api/trending/post/{days}
#### GET
Returns trending posts from last {days} days.

Success code: ```200```
      
Error code:

```404``` - not found

Example:
```
[
    {
        "pk": 8,
        "owner": {
            "pk": 1,
            "username": "admin",
            "profile_picture": "/media/media/user_1/profile/cattt605281251_U5Yl9sR.jpg",
            "name": "Admin AGH",
            "bio": "Im admin of this platform",
            "followers": 0,
            "follows": 2
        },
        "description": "postman test, utw with a very cool photo",
        "picture": "/media/media/user_1/posts/1_SzViXwd.jpg",
        "date": "2022-12-03T17:37:41.045722Z",
        "no_of_likes": 1
    },
    ...
]
```

### /api/trending/users
#### GET
Returns popular users from last {days} days.

Success code: ```200```
      
Error code:

```404``` - not found
    
Example:
```
[
    {
        "pk": 15,
        "username": "igorniebtest1",
        "profile_picture": "/media/media/blank.png",
        "name": "",
        "bio": "",
        "followers": 0,
        "follows": 0
    },
    ...
]
```

### /api/search/{query}
#### GET
Returns users with usernames matching given query.

Success code: ```200```
      
Error code:

```404``` - not found
    
Example:
```
[
    {
        "pk": 15,
        "username": "igorniebtest1",
        "profile_picture": "/media/media/blank.png",
        "name": "",
        "bio": "",
        "followers": 0,
        "follows": 0
    },
...
]
```

### /api/notifications
#### GET
Returns the latest actions related to logged-in user

Success code: ```200```
      
Error code:

```403``` - access denied

```404``` - not found

Example:
```
[
    {
        "content_user": {
            "pk": 1,
            "username": "admin",
            "profile_picture": "/media/media/user_1/profile/cattt605281251_U5Yl9sR.jpg",
            "name": "Admin AGH",
            "bio": "Im admin of this platform",
            "followers": 0,
            "follows": 2
        },
        "verb": "commented",
        "content_object": {
            "comment_pk": 46,
            "owner": {
                "pk": 1,
                "username": "admin",
                "profile_picture": "/media/media/user_1/profile/cattt605281251_U5Yl9sR.jpg",
                "name": "Admin AGH",
                "bio": "Im admin of this platform",
                "followers": 0,
                "follows": 2
            },
            "post": {
                "pk": 9,
                "owner": {
                    "pk": 1,
                    "username": "admin",
                    "profile_picture": "/media/media/user_1/profile/cattt605281251_U5Yl9sR.jpg",
                    "name": "Admin AGH",
                    "bio": "Im admin of this platform",
                    "followers": 0,
                    "follows": 2
                },
                "description": "hmm smh is wrong...",
                "picture": "/media/media/user_1/posts/honda-hrc.jpg",
                "date": "2022-12-03T17:42:52.653233Z",
                "no_of_likes": 0
            },
            "comment": "New comment",
            "date": "2022-12-06T20:08:10.990633Z"
        }
    },
   ...
]
```
### /api/register
#### POST
Registration for new users

Success code: ```201```

Error code:

```3``` - smh

Example: 
```
{
    "username": "username",
    "email": "username@mail.ii",
    "password1": "password",
    "password2": "password"
}
```

### login/authentication
This app uses baisic authentication methods.
