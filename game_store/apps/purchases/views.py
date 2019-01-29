from django.shortcuts import render

def purchase(req, id):
    return render(req, 'purchase.html')

def stats(req):
    return render(req, 'stats.html')
