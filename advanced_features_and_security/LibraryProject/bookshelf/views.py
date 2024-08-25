from django.shortcuts import render
from .models import Book, CustomPermission
from django.utils import timezone
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django import forms
# Create your views here.
def create_Book(request):
    Book.objects.create(title= "1984", author= "George Orwell",publication_year= 1949)
    #SELECT * from Book
    Book.objects.all()


@permission_required('CustomPermission.can_edit', raise_exception=True)
def edit_view(request, pk):
    # Code to handle the edit action
    instance = CustomPermission.objects.get(pk=pk)
    if request.method == 'POST':
        # Process form data
        pass
    return render(request, 'edit_template.html', {'instance': instance})

@permission_required('CustomPermission.can_create', raise_exception=True)
def create_view(request):
    # Code to handle the create action
    if request.method == 'POST':
        # Process form data
        pass
    return render(request, 'create_template.html')

@permission_required('CustomPermission.can_view', raise_exception=True)
def view_view(request, pk):
    # Code to handle the view action
    instance = CustomPermission.objects.get(pk=pk)
    return render(request, 'view_template.html', {'instance': instance})

@permission_required('your_app.can_delete', raise_exception=True)
def delete_view(request, pk):
    # Code to handle the delete action
    instance = CustomPermission.objects.get(pk=pk)
    if request.method == 'POST':
        instance.delete()
        return redirect('some_view')
    return render(request, 'delete_template.html', {'instance': instance})


''' "book_list", "books" ''' 

from django.shortcuts import get_object_or_404
from .models import Book

def my_view(request, id):
    obj = get_object_or_404(Book, pk=id)
    return render(request, 'form_example.html', {'object': obj})

class MyForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['field1', 'field2']

def my_form_view(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            form.save()
            # Handle successful form submission
    else:
        form = MyForm()
    return render(request, 'form_example.html', {'form': form})
MIDDLEWARE = [
    'csp.middleware.CSPMiddleware',
    # other middlewares
]