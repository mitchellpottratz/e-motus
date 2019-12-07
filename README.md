# e-motus

## Description
This is the Flask API for the Emotus React app. Emotus is a social media app which allows you to post status updates which
consist of a brief description of something that happened, or something that is on you mind, alongside emotional word of how it made you feel, and emojis. Users can follow eachother, views eachothers posts, likes posts, comment on posts, etc. 


## Routes 

### /users Routes
|  URL  | HTTP Verb | RESTful Action |      Description      | 
|-------|-----------|--------|-----------------------|
| /users/login/ | POST | login | Logs in an existing user |
| /users/register/ | POST | register | Registers a new user |
| /users/logout/ | GET | logout | Logs out a user |

### /posts Routes
|  URL  | HTTP Verb | RESTful Action |      Description      | 
|-------|-----------|--------|-----------------------|
| /posts/ | GET | index | Gets all of the current users posts |
| /posts/feed/ | GET | - | Gets all post from users the current user follows |
| /posts/ | POST | create | Creates a new post |
| /posts/{postId}/ | GET | show | Gets a single post |
| /posts/{postId}/ | PUT | update | Updates a post |
| /posts/{postId}/ | DELETE | delete | Deletes a post |

### /likes Routes
|  URL  | HTTP Verb | RESTful Action |      Description      | 
|-------|-----------|--------|-----------------------|
| /likes/ | GET | index | Gets all of the likes for a post |
| /likes/user/ | GET | - | Gets all posts the current user has liked |
| /likes/ | POST | create | Creates a new like for a post |
| /likes/{likeId}/ | GET | show | Gets a single like |
| /likes/{likeId} | DELETE | delete | Deletes a like for a post |

### /follows Routes
|  URL  | HTTP Verb | RESTful Action |      Description      | 
|-------|-----------|--------|-----------------------|
| /follows/followers/ GET | - | Gets all of current users followers |
| /follows/following/ | GET | - | Gets all user the current user is following |
| /follows/ | POST | create | Creates a follow between current user and another user |
| /follows/{userId}/ | DELETE | delete | Deletes a follow between current user and another user |

### /comments Routes
|  URL  | HTTP Verb | RESTful Action |      Description      | 
|-------|-----------|--------|-----------------------|
| /comments/{postId}/ | GET | index | Gets all of the comments for a post |
| /comments/user/{postId}/ | GET | - | Gets all comments created by the current user for a single post |
| /comments/ | POST | create | Creates a new comment |
| /comments/{commentId}/ | DELETE | delete | Deletes a comment |


