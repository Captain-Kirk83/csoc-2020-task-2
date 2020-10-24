from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg,Count
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from datetime import date

# Create your views here.

def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    context = {
        'book': None, # set this to an instance of the required book
        'num_available': None, # set this to the number of copies of the book available, or 0 if the book isn't available
    }
    # START YOUR CODE HERE
    obj=Book.objects.get(id=bid)
    context['book']=obj
    try:
        context['num_available']=BookCopy.objects.filter(book__title=obj.title).filter(status=True).count()
    except BookCopy.objects.get(book__title=obj.title).DoesNotExist:
        context['num_available']=0

    
    
    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    context = {
        'books': None, # set this to the list of required books upon filtering using the GET parameters
                       # (i.e. the book search feature will also be implemented in this view)
    }
    get_data = request.GET
    # START YOUR CODE HERE
    

    
    try:
        context['books']=Book.objects.filter(title=get_data['title']).filter(author=get_data['author']).filter(genre=get_data['genre'])
    except MultiValueDictKeyError:
        context['books']=Book.objects.all()
    
    
    return render(request, template_name, context=context)

@login_required
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
    context = {
        'books': None,
    }
    '''
    The above key 'books' in the context dictionary should contain a list of instances of the 
    BookCopy model. Only those book copies should be included which have been loaned by the user.
    '''
    # START YOUR CODE HERE
    try:
        context['books']=BookCopy.objects.filter(borrower=request.user)
        return render(request, template_name, context=context)
    except AttributeError:
        return HttpResponse('No book loaned')


@csrf_exempt
@login_required
def loanBookView(request):
    response_data = {
        'message': None,
    }
    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
    # START YOUR CODE HERE
    book_id = None # get the book id from post data
    book_id = request.POST['bid']
    obj=Book.objects.get(id=book_id)
    obj1=BookCopy.objects.filter(book__id=obj.id).filter(status=True)
    if(obj1.count==0):
        response_data['message']='failure'
    else:
        
        obj1[0].saves('False',request.user,date.today())
        obj1[0].save()
        
        response_data['message']='success'

    return JsonResponse(response_data)

'''
FILL IN THE BELOW VIEW BY YOURSELF.
This view will return the issued book.
You need to accept the book id as argument from a post request.
You additionally need to complete the returnBook function in the loaned_books.html file
to make this feature complete
''' 
@csrf_exempt
@login_required
def returnBookView(request):
    template_name = 'store/loaned_books.html'
    get_data = request.POST
    obj=BookCopy.objects.filter(book__id=get_data['bid'])
    if(obj.count!=0):
        for i in obj:
            if(i.status==False):
                i.saves('True',None,None)
                i.save()
                break
    response_data = {
        'message': 'success',
        }
        
    return JsonResponse(response_data)


@login_required
def ratereview(request):
    bks = Book.objects.order_by('title').annonate(rating=Avg('RateModel__bookRate'))
    context = { 'book': bks}

    return render(request, 'store/book_detail.html', context=context)

@login_required
def rateBook(request):
    book_id=request.POST['bid']
    obj=RateModel.booktoRate.objects.get(pk=book_id)
    obj.bookRate=request.POST['rate']
    print(obj)
    return JsonResponse(obj)
