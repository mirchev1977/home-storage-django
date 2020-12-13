# home_storage_django rest API receiving requests from the angular front-end deployed currently on: http://mirchev-home-storage-ang.herokuapp.com/

# CURL REQUESTS

#create new user
!curl -X POST -d 'id=1' -d 'email=ivan@ivan.com' -d 'name=Ivan Ivanv' -d 'password=ivan_pass' -d 'role=user' -d 'token=1234' http://127.0.0.1:8000/users/new

#user login
!curl -X POST -d 'email=ivan@ivan.com' -d 'password=ivan_pass' http://127.0.0.1:8000/user/login

#user delete
!curl -i GET -H 'Authorization: 4cfdc14aa2d807839c85efc22fa2b2f4e8f72648;;pesho@pesho.com;;user' http://127.0.0.1:8000/users/24/delete
#r !curl -i POST -H 'Authorization: e0106b7b3ce8b8d173062a7f6f79affed2c74066;;pesho@pesho.com;;user' http://127.0.0.1:8000/users/22/delete
#r !curl -i GET http://127.0.0.1:8000/users/22/delete

#user update
!curl -X POST -H 'Authorization: 11b7a22272ab80d8dce0a19f4eb223c7c1459479;;ivan@ivan.com;;user' -d 'id=1' -d 'email=ivan@ivan.com' -d 'name=Ivan Ivanov' -d 'password=tralalalala' -d 'role=user' -d 'token=1234' http://127.0.0.1:8000/users/27/update


#users all
!curl -i GET -H 'Authorization: 11b7a22272ab80d8dce0a19f4eb223c7c1459479;;pesho@pesho.com;;user' http://127.0.0.1:8000/users/all

#user logout
!curl -i GET -H 'Authorization: 8de4c81924777237e3ec0cbdb3d734e72e6e1707;;ivan@ivan.com;;user' http://127.0.0.1:8000/user/logout


#location update
!curl -X POST -H 'Authorization: 868800e235b8d72093cc727f9ac1588c2cf62f05;;ivan@ivan.com;;user' -d 'creator=27' -d 'id=undefined' -d 'imgUrl=https://www.olxgroup.com/assets/styles/hero/public/2018-07/SOFIA.jpg?itok=_l_lkHR9' -d 'location=Two' -d 'privacy=public' http://127.0.0.1:8000/locations/3/update

#locations all
!curl -i GET http://127.0.0.1:8000/locations/all


#container new
!curl -X POST -H 'Authorization: 868800e235b8d72093cc727f9ac1588c2cf62f05;;ivan@ivan.com;;user' -d 'coords={col:27,row:28}' -d 'creator=27' -d 'description=one' -d 'id=' -d 'imgLink=https://mccontainers.com/wp-content/uploads/2018/04/50102.jpg' -d 'items=undefined' -d 'location=2' -d 'privacy=public' -d 'url=https://mccontainers.com/wp-content/uploads/2018/04/50102.jpg' -d 'vertical=горе' http://127.0.0.1:8000/containers/new


#containers all
!curl -i GET http://127.0.0.1:8000/containers/all

#container delete
!curl -i GET -H 'Authorization: 868800e235b8d72093cc727f9ac1588c2cf62f05;;pesho@pesho.com;;user' http://127.0.0.1:8000/containers/1/delete

#container update
!curl -X POST -H 'Authorization: 868800e235b8d72093cc727f9ac1588c2cf62f05;;ivan@ivan.com;;user' -d 'coords={col:27,row:28}' -d 'creator=27' -d 'description=one' -d 'id=' -d 'imgLink=https://mccontainers.com/wp-content/uploads/2018/04/50102.jpg' -d 'items=undefined' -d 'location=2' -d 'privacy=public' -d 'url=https://mccontainers.com/wp-content/uploads/2018/04/50102.jpg' -d 'vertical=горе' http://127.0.0.1:8000/container/4/update


#container searchItem
!curl -X POST -H 'Authorization: 868800e235b8d72093cc727f9ac1588c2cf62f05;;ivan@ivan.com;;user' -d 'location=2' http://127.0.0.1:8000/search/items?searchTerm=Four

#item new
!curl -X POST -H 'Authorization: 868800e235b8d72093cc727f9ac1588c2cf62f05;;ivan@ivan.com;;user' -d 'description=one' -d 'id=' -d 'imgUrl=https://mccontainers.com/wp-content/uploads/2018/04/50102.jpg'  -d 'container=12' http://127.0.0.1:8000/item/new

#item update
!curl -X POST -H 'Authorization: 868800e235b8d72093cc727f9ac1588c2cf62f05;;ivan@ivan.com;;user' -d 'description=description of item 1' -d 'id=' -d 'imgUrl=https://mccontainers.com/wp-content/uploads/2018/04/50102.jpg'  -d 'container=12' http://127.0.0.1:8000/item/5/update


#item delete
!curl -i GET -H 'Authorization: 868800e235b8d72093cc727f9ac1588c2cf62f05;;ivan@ivan.com;;user' http://127.0.0.1:8000/item/1/delete

#items -get all
!curl -i GET -H 'Authorization: 868800e235b8d72093cc727f9ac1588c2cf62f05;;ivan@ivan.com;;user' http://127.0.0.1:8000/items/12/all?searchTerm=of




#item upload image
!curl -X POST -H 'Authorization: 868800e235b8d72093cc727f9ac1588c2cf62f05;;ivan@ivan.com;;user' -d 'image=okokokok' http://127.0.0.1:8000/items/uploadFile
