# socialplatform
## 1. Descryption
social platform made using Django with REST API and Bootstrap frontend.

social platform is a photo social service. It lets you host your own pictures, follow other users and like their posts.
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
   
   Succes code: 200
   
   Error code: 404
   
   Example:
   
      ```{
            "pk": 1,
            "username": "admin",
            "profile_picture": "/media/media/user_1/profile/cattt605281251_U5Yl9sR.jpg",
            "name": "Admin AGH",
            "bio": "Im admin of this platform",
            "followers": 0,
            "follows": 2
         }```
### /api/user/follows/{id}
  #### GET
   Returns list of users that user with a given id follows.
   
   Succes code: 200
   
   Error code: 404
   
   Example:
   
      ```[
          {
              "follower": "admin",
              "follower_url": "/user/1",
              "followed": "igorniebylski",
              "followed_url": "/user/14"
          },
          ...
         ]```
### /api/user/followers/{id}
  #### GET
   Returns list of users that are followin user with a given id.
   
   Succes code: 200
   
   Error code: 404
   
   Example:
   
      ```[
          {
              "follower": "admin",
              "follower_url": "/user/1",
              "followed": "igorniebylski",
              "followed_url": "/user/14"
          },
          ...
         ]```
### /api/settings
  #### GET
   Lets logged in user view their account info.
   
   Succes code: 200
   
   Error code: 403
   
   Example:
   
      ```{
          "pk": 1,
          "username": "admin",
          "profile_picture": "/media/media/user_1/profile/cattt605281251_U5Yl9sR.jpg",
          "name": "Admin",
          "bio": "Im admin of this platform",
          "followers": 0,
          "follows": 2
         }```
### /api/settings
  #### PATCH
   Lets logged in user update their account info.
   
   Succes code: 200
   
   Error code:
   
   ```403``` user is not authenticated
   
   ```400``` wrong input
   
   Example:
   
      ```{
          "profile_picture": "/media/media/user_1/profile/cattt605281251_U5Yl9sR.jpg",
          "name": "Admin",
          "bio": "Im admin of this platform",
         }```
### /follow/{id}
  #### GET
   Follows/unfollows user with a given id
   
   Succes code: 200, 201
   
   Error code: 
   
    ```404``` user not found
    
   ```403``` user is not authenticated
   
   ```400``` other error
   
 ### /post/{id}
  #### GET
   Gets post with given id.
   
   Succes code: 200
   
   Error code: 
   
    ```404``` post not found
    
   ```403``` user is not authenticated
   
   ```400``` bad request
   
   Example:
   
     ```{
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
  }```
  
  #### PATCH
   Lets owner edit their post description.
   
   Succes code: 200
   
   Error code: 
   
    ```404``` post not found
    
   ```403``` user is not authenticated
   
   ```400``` bad request
   
   Example:
   
     ```{
      "description": "My new kaczkaa",
    }```
  #### DELETE
   Deletes post with given id.
   
   Succes code: 204
   
   Error code: 
   
    ```404``` post not found
    
   ```403``` user is not authenticated
   
   ### /post/comments/{id}
  #### GET
   Gets comments related to post with given id.
   
   Succes code: 200
   
   Error code: 
   
    ```404``` post not found
         
   Example:
   
     ```[
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
  ]```
  
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
###/api/comment/{id}
      ####GET
      Gets comment with given id.
      
      Succes code: ```200```
      
      Error code:
      
      ```404``` comment not found
      
      Example:
      ```{
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
    }'''
  ####PATCH
  Lets owner edit comment with given id.
  
  Succes code: 200
      
  Error code:
      
  ```404``` comment not found
  ```403``` user is not authenticated
  ```400``` bad request
  
  Example:
  ```{
  'comment':'edit comment'
  }```
  
  ####DELETE
  Deletes comment with given id.
  
  Succes code: 204
            
  Error code:
  
  ```404``` comment not found
  ```403``` user is not authenticated
  
  
  
      
  

    
         
         
   
    
