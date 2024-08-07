from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.conf import settings
from . models import Movie, MovieList
import re

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    featured_movie = movies[len(movies)-1]
    
    context = {
        'movies': movies,
        'featured_movie': featured_movie,  # Add this line
    }
    
    return render(request, 'index.html', context, )



@login_required  # you can also use this as >> @login_required(login_url='login')  if you did not specify login url in settings.py
def movie(request, pk):
    movie = Movie.objects.get(uu_id=pk)

    if not movie:
        return redirect('/')
    
    context = {
       'movie_details': movie,
    }
    return render(request,'movie.html', context)



# @login_required
# def my_list(request):
#     pass



@login_required
def add_to_list(request):
    if request.method == 'POST':
        movie_url_id = request.POST['movie_uuid']

        uuid_pattern = r"[-0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
        match = re.search(uuid_pattern, movie_url_id)
        movie_uuid = match.group() if match else None

        # quickly search for uuid in db esle return 404
        movie = get_object_or_404(Movie, uu_id=movie_uuid)
        movie_url_list, created = MovieList.objects.get_or_create(owner = request.user, movie=movie)

        if created:
            messages.success(request, 'Movie added to your list')
            response = {
                "code": 200,
                "status": "success",
                "message": "Movie added successfully",
                "movie": created
            }
        else:
            response = {
                "code": 400,
                "status": "failed",
                "message": "Movie already in your list",
                "movie": []
            }
            messages.info(request, 'Movie already in your list')

        return JsonResponse(response)   
    
    output = {
        "code": 400,
        "status": "failed",
        "message": "Only POST requests are allowed",
        "movie": []
    }    
    return JsonResponse(output) 




@login_required(login_url="login")
def my_list(request):

    movies = MovieList.objects.filter(owner = request.user)
    user_movie_list = []
    
    for movie in movies:
        # user_movie_list.append({
        #     "id": movie.id,
        #     "movie": movie.movie.title,
        #     "uu_id": movie.movie.uu_id
        # })
        user_movie_list.append(movie.movie) #this is simple to use this way
    context = {
        "movies": user_movie_list
    }

    return render(request, 'my_list.html', context)




@login_required(login_url="login")
def search(request):
    if request.method == 'POST':
        search_query = request.POST['search']
        movies = Movie.objects.filter(title__icontains=search_query)
        context = {
            'search_term': search_query,
            'movies': movies
        }
        return render(request,'search.html', context)
    
    return redirect('/')





@login_required 
def genre(request, pk):
    movies = Movie.objects.filter(genre=pk)

    if not movie:
        return redirect('/')
    
    context = {
       'movies': movies,
       'genre': pk,
    }
    return render(request,'genre.html', context)





def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']
        
        if password == password_confirmation:
            try :
                if User.objects.filter(email = email).exists():
                    messages.info(request, 'Email already exists')
                    return redirect('signup')
                elif User.objects.filter(username = username).exists():
                    messages.info(request, 'Username already exists')
                    # error_message = 'Username already exists'
                    return redirect('signup')
                
                user = User.objects.create_user(username, email, password)
                user.save()
                
                # login(request, user)

                messages.success(request, 'Registration successful. You can login now.')
                # return redirect('/', user)'Error occurred while registering user'
                return redirect('signup')
            except Exception as e:
                print(f'Error occurred while registering user: {e}')

                messages.info(request, e)
                return redirect('signup')
        
        messages.info(request, 'The passwords you entered does not match')
        # error_message = 'The passwords you entered does not match'
        return redirect('signup')
    return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username = username, password = password)
        #user = authenticate(username = username, password = password)# use only if you imported authentication, login, logout = from django.contrib.auth import authenticate, login, logout
        if user is not None:
            auth.login(request, user)
            # login(request, user) # use only if you imported authentication, login, logout = from django.contrib.auth import authenticate, login, logout
            messages.success(request, 'Login successful')
            return redirect('/', user)
        else:
            # error_message = 'Username or password is incorrect'
            messages.info(request, 'Username or password is incorrect')
            return redirect('login')
        
    return render(request, 'login.html')


@login_required
def user_logout(request):
    #logout(request) all works since we imported logout directly
    auth.logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('login')
