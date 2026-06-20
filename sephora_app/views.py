from django.shortcuts import render,redirect
from .models import UserRegister,Product
def index(request):
    return render(request,'index.html')
def home(request):
    products = Product.objects.all()
    return render(request,'home.html', {'products': products})

# Create your views here.

def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        profile_pic = request.FILES.get('profile_pic')

        UserRegister.objects.create(
            name=name,
            email=email,
            password=password,
            profile_pic=profile_pic
        )

        return redirect('home')

    return render(request, 'register.html')


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email,password)

        try:
            user = UserRegister.objects.get(
                email=email,
                password=password
            )

            # Store user id in session
            print(user.email)
            request.session['email'] = user.email

            return redirect('home')  # Change to your home page URL name

        except UserRegister.DoesNotExist:
            print("Invalid email or password")
            return render(request, 'login.html', {
                'error': 'Invalid email or password'
            })

    return render(request, 'login.html')


def profile(request):
    email = request.session.get('email')

    if email:
        user = UserRegister.objects.get(email=email)

        context = {
            'user': user
        }
        return render(request, 'profile.html', context)

    return render(request, 'login.html')
from django.shortcuts import render, redirect, get_object_or_404


from django.shortcuts import render, redirect, get_object_or_404
from .models import UserRegister

def edit_profile(request, id):
    user = get_object_or_404(UserRegister, id=id)

    if request.method == "POST":
        user.name = request.POST.get("name")
        user.email = request.POST.get("email")

        if request.FILES.get("profile_pic"):
            user.profile_pic = request.FILES.get("profile_pic")

        user.save()

        return redirect('home')

    return render(request, 'edit_profile.html', {'user': user})

def add_product(request):
    email = request.session.get('email')
    user = UserRegister.objects.get(email=email)

    if request.method == 'POST':
        Product.objects.create(
            user=user,
            product_name=request.POST.get('product_name'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            stock=request.POST.get('stock'),
            product_image=request.FILES.get('product_image')
        )

        return redirect('home')

    return render(request, 'add-product.html')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})
  

def my_products(request):
    products = Product.objects.all()

    return render(request, 'my_products.html', {'products': products
    })
     
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.product_name = request.POST.get('product_name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')

        # Only if your model has a stock field
        product.stock = request.POST.get('stock')

        if request.FILES.get('product_image'):
            product.product_image = request.FILES['product_image']

        product.save()

        return redirect('my_products')

    return render(request, 'edit_product.html', {
        'product': product
    })
def delete_product(request, product_id):
    email = request.session.get('email')
    user = UserRegister.objects.get(email=email)
    product = get_object_or_404(
        Product,
        id=product_id,
        user=user
    )

    product.delete()

    return redirect('my_products')