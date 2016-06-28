from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.db.models import Count, Sum
from .models import User, Poke
# Create your views here.
def index(request):
	return render(request, 'index.html')
def register(request):
	if request.method == 'POST':
		user = User.userManager.register(request.POST['name'], request.POST['alias'], request.POST['email'], request.POST['password'], request.POST['confirm_password'])
		context = {'errors' : user[1]}
		if user[0]:
			request.session['id'] = user[1].id
			request.session['name'] = user[1].name
	return render(request, 'index.html', context)
def login(request):
	if request.method =='POST':
		user_tuple = User.userManager.login(request.POST['email'], request.POST['password'])
		context = {
			'login': user_tuple[1]
		}
		if user_tuple[0]:
			request.session['id'] = user_tuple[1].id
			request.session['name'] = user_tuple[1].name
			return redirect(reverse('pokes'))
		else:
			print 'does not work'
			return render(request, 'index.html', context)
def pokes(request):
	user = User.userManager.all()
	pokes = {}
	for myuser in user:
		pokes[myuser.id] = myuser.f2.all().aggregate(Sum('poke'))
	context ={
		'user' : user,
		'poke' : Poke.objects.all(),
		'pokes' : pokes
	}


	return render(request, 'poke.html', context)

def poke(request, id):
		print request.session['id'] # current logged in user (poker)
		print id # current person being poked.
		try:
			pokeEvent = Poke.objects.get(user1=request.session['id'], user2=id)
			pokeEvent.poke = pokeEvent.poke + 1
			pokeEvent.save()
			print "update poke #"
		except:
			loggedInUser = User.userManager.get(id=request.session['id'])
			pokedUser = User.userManager.get(id=id)
			Poke.objects.create(user1=loggedInUser,user2=pokedUser)
			print "create new poke"
		return redirect(reverse('pokes'))
