from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse

from catalogue.forms import ProductSearchForm, ProductEditForm
from catalogue.models import Product


def product_list(request):
    products = Product.objects.order_by('name')

    form = ProductSearchForm(request.GET)
    products = form.filter_products(products)

    params = request.GET.copy()
    if 'page' in params:
        page = params['page']
        del params['page']
    else:
        page = 1
    search_params = params.urlencode()

    paginator = Paginator(products, 5)
    try:
        products = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        products = paginator.page(1)

    return TemplateResponse(request, 'catalogue/product_list.html',
                            {'products': products,
                             'form': form,
                             'search_params': search_params})


def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404
    return TemplateResponse(request, 'catalogue/product_detail.html',
                            {'product': product})


def product_edit(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = ProductEditForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('product_detail',
                                                args=(product.id,)))
    else:
        form = ProductEditForm(instance=product)
    return TemplateResponse(request, 'catalogue/product_edit.html',
                            {'form': form, 'product': product})


def product_delete(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        product.delete()
        return HttpResponseRedirect(reverse('product_list'))
    else:
        return TemplateResponse(request, 'catalogue/product_delete.html',
                                {'product': product})