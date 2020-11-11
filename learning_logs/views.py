from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from operator import attrgetter

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Base page


def index(request):

    return render(request, 'learning_logs/index.html')
# Topics


@login_required
def topics(request):
    # Order the data by its date time
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    # Displays data
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)
# Entry


@login_required
def topic(request, topic_id):
    # gets the topic id
    topic = get_object_or_404(Topic, id=topic_id)
    # Order the data by its date time but in reverse
    entries = topic.entry_set.order_by('-date_added')
    # Displays data
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)
# Allows the user to Enter a Topic


@login_required
def new_topic(request):
    # Check whether its a POST request or a GET request
    if request.method != 'POST':
        # Returns a blank
        form = TopicForm()

    else:
        # Saving the data in request.POST
        form = TopicForm(request.POST, request.FILES)
        # Checks whether the data that have been submitted mach the default Setting in models
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            # Returns the user to the topics page
            return redirect('learning_logs:topics')
    # Displaying the data
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)
# Allows the user to Enter a Entry


@login_required
def new_entry(request, topic_id):
    # Getting the topic id
    topic = Topic.objects.get(id=topic_id)
    # Checks if user
    check_topic_user(request, topic)
    # Checks whether its a POST or GET request
    if request.method != 'POST':
        # Returns blank
        form = EntryForm()

    else:
        # Save data in POST request
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # Assign data to new entry without saving them yez
            new_entry = form.save(commit=False)
            # Saves the entry to its topic
            new_entry.topic = topic
            new_entry.owner = request.user
            new_entry.save()
            # Redirect/returns the user to the entry page
            return redirect('learning_logs:topic', topic_id=topic_id)
    # Displaying the data
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_topic(request, topic_id):
    # Getting the topic id
    topic = Topic.objects.get(id=topic_id)
    # Checking if the user matches the topic
    check_topic_user(request, topic)
    if request.method != 'POST':
        form = TopicForm(instance=topic)
    else:
        form = TopicForm(request.POST, request.FILES, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_topic.html', context)

# Editing info/entries


@login_required
def edit_entry(request, entry_id):
    # Getting the entry id
    entry = Entry.objects.get(id=entry_id)
    # Signing the entry to topic
    topic = entry.topic
    # Checks if user
    check_topic_user(request, topic)
    # Checking the request type
    if request.method != "POST":
        form = EntryForm(instance=entry)

    else:
        # Saving the data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    # Displaying data
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
def delete_topic(request, topic_id):
    # Check method
    if request.method == 'POST':
        # get topic id
        topic = Topic.objects.get(id=topic_id)
        check_topic_user(request, topic)
        # delete topic
        topic.delete()
    # redirect user to the topics page
    return redirect('learning_logs:topics')


@login_required
def delete_entry(request, entry_id):
    # Check method
    if request.method == 'POST':
        # get the entry id
        entry = Entry.objects.get(id=entry_id)
        check_topic_user(request, entry)
        # delete entry
        entry.delete()
    # redirect the user to the entry page
    return redirect('learning_logs:topics')


@login_required
def upload(request):
    context = {}
    if request == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'learning_logs/upload.html', context)


@login_required
def search(request):
    query = request.GET.get('q')

    if query:
        result = Topic.objects.filter(Q(text__icontains=query))
        context = {'query': query, 'result': result}
        return render(request, 'learning_logs/search.html', context)


def check_topic_user(request, topic):
    # Raises error if not user
    if topic.owner != request.user:
        raise Http404
