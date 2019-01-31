from django.shortcuts import render

def leaderboards(req):
    return render(req, 'leaderboards.html')
