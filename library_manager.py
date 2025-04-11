import streamlit as st
import pandas as pd
import json
import os
import datetime
import requests
import time
import plotly.express as px
import plotly.graph_objects as go  
from streamlit_lottie import st_lottie
# set page configuration
st.set_page_config(page_title="Personal Library Management System", 
     page_icon="📚", 
    layout="wide",
    initial_sidebar_state="expanded")

# custom css
st.markdown("""
<style>
       .main-header {
            font-size: 3rem !important;
            font-weight: 700;
            color: #000000;
            text-align: center;
            margin-bottom: 2rem;
         text-shadow: 2px 2px 4px rgba(0, 0, 0, 1);
        
            
        }

        .sub-header {
            font-size: 1.5rem !important;
            font-weight: 600;
            color: #3BB2DF6;
            text-align: center;
            margin-bottom: 1rem;
            margin-top: 1rem;
        } 
        .sucess-message {
            padding: 1rem;
            background-color: #FEF#C7
            border-left: 5px solid #F59E0b;
            border-radius: 0.375em;
    
        }        

        .book-card {
            background-color: #F3F4F6
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
            border-left: 5px solid #3BB2f6;
            transition: transform 0.3s ease;
        }

        .book-card-hover{
            transform: translate(-5px);
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        }

        .read-bage {
            background-color: #10B981;
            color:white;
            paddding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.875rem;
            font-weight: 600; 
        

        }        

        .unread-bage{
             background-color: #F87171;
            color:white;
            paddding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.875rem;
            font-weight: 600; 
        
            
        }
        .action-button{
            border-radius: 0.375rem;

            }
            </style>
            
""",unsafe_allow_html=True)

# part 2

def load_lottleurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None
    
if'library' not in st.session_state:
    st.session_state.library = []
if'search_results' not in st.session_state:
     st.session_state.search_results = []
if'book_added' not in st.session_state:
     st.session_state.book_added = False
if'book_removed' not in st.session_state:
     st.session_state.book_removed = False
if'current_view' not in st.session_state:
     st.session_state.current_view = "library" 


# load library
def load_library():
    try:
        if os.path.exists("library.json"):
            with open("library.json", "r") as file:
                st.session_state.library = json.load(file)
            return True
        return False
    except Exception as e:
        st.error(f"Error loading library: {e}")
        return False
    except Exception as e:
        st.error(f"Error loading library: {e}")
        return False
    
# save library
def save_library():
    try:
        with open("library.json", "w") as file:
            json.dump(st.session_state.library, file)
        st.session_state.book_added = True
    except Exception as e:
        st.error(f"Error saving library: {e}")


#add book to library
def add_book(title, author, publication_year, genre, read):
    book = {
        "title": title,
        "author": author,
        "publication_year": publication_year,
        "genre": genre,
        "read": read,
        "added_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.library.append(book)
    save_library()
    st.session_state.book_added = True
    time.sleep(0.5)
    st.success("Book added successfully!") 


#remove book from library
def remove_book(index):
    if 0 <= index < len(st.session_state.library):


        del st.session_state.library[index]
        save_library()
        st.session_state.book_removed = True
        time.sleep(0.5)
        st.success("Book removed successfully!")
    else:
        st.error("Invalid book index.")


# search book in library
def search_book(search):
    search_term = search_term.lower()
    results = []

    for book in st.session_state.library:
        if search_by == "Title" and search_term in book["title"].lower():
            results.append(book)
        elif search_by == "Author" and search_term in book["author"].lower():
            results.append(book)  
        elif search_by == "Genre" and search_term in book["genre"].lower():
            results.append(book)
        st.session_state.search_results = results

# calculate library state
def get_library_state():
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book["read status"])
    percent_read = (read_books / total_books) * 100 if total_books > 0 else 0


    generes = {}
    authors = {}
    decades = {}


    for book in st.session_state.library:
        if book["genre"] not in generes:
            generes[book["genre"]] += 1
        else:
            generes[book["genre"]] = 1

    # count authors
    if book["author"] not in authors:
            authors[book["author"]] += 1
    else:
            authors[book["author"]] = 1   
    #  count decades

    decade = (book["publication_year"] // 10) * 10
    if decade not in decades:
        decades[decade] += 1
    else:
        decades[decade] = 1

# sort by count

    generes = dict(sorted(generes.items(), key=lambda item: item[1], reverse=True))
    authors = dict(sorted(authors.items(), key=lambda item: item[1], reverse=True))
    decades = dict(sorted(decades.items(), key=lambda item: item[1], reverse=True))

    return {
        'total_books': total_books,
        'read_books': read_books,
        'percent_read': percent_read,
        'generes': generes,
        'authors': authors,
        'decades': decades
    }

def create_visulations(stats):
    if stats['total_books'] > 0:
       fig_read_status = go.Figure(data=[go.Pie(
           labels=['Read', 'Unread'],
           values=[stats['read_books'], stats['total_books'] - stats['read_books']],
           hole=0.4,
           marker_colors=['#10B981', '#F87171']
           )])
       fig_read_status.update_layout(
              title_text="Read vs Unread Books",
              showlegend=True,
              height=400   
         )
       st.plotly_chart(fig_read_status, use_container_width=True)
    #    bar chart for genres

    if stats['generes']:
        genres_df = pd.DataFrame({
            'Genre': list(stats['generes'].keys()),
            'Count': list(stats['generes'].values())
        })
        fig_genres = px.bar(
            genres_df,
            x='Genre',
            y='Count',
            title="Books by Genre",
            color='Count',
            color_continuous_scale=px.colors.sequential.Viridis
        )
        fig_genres.update_layout(
            title_text="Books by  publication generes",
            xaxis_title="Genres",
            yaxis_title="Number of books",
            height=400
        )
        st.plotly_chart(fig_genres, use_container_width=True)
    if stats['decades']:
        decades_df = pd.DataFrame({
            'Decade': [f"{decade}s" for decade in stats['decades'].keys()],
            'Count': list(stats['decades'].values())
        })
        fig_decades = px.line(
            decades_df,
            x='Decade',
            y='Count',
            markers=True,
            line_sape="spline"
        )
        fig_decades.update_layout(
            title_text="Books by publication Decade",
            xaxis_title="Decade",
            yaxis_title="Number of books",
            height=400
        )
        st.plotly_chart(fig_decades, use_container_width=True)

        # load library
load_library()
st.sidebar.markdown("<h1 style='text-align: center;'> Navigation</h1>", unsafe_allow_html=True)
lottie_book = load_lottleurl("https://assets3.lottiefiles.com/packages/lf20_4j7v1g5h.json") 
if lottie_book:
    st_lottie(lottie_book, height=200, width=200, key="book animation")

nav_options = st.sidebar.radio(
    "Select an option",
    ["View Library", "Add Book", "Search Book", "Statistics"])

if nav_options == "View Library":
    st.session_state.current_view = "library"
elif nav_options == "Add Book":
    st.session_state.current_view = "add_book" 
elif nav_options == "Search Book":
    st.session_state.current_view = "search"
elif nav_options == "Statistics":
    st.session_state.current_view = "statistics"  


st.markdown("<h1 class='main-header'>Personal Library Management System</h1>", unsafe_allow_html=True)
if st.session_state.current_view == "add":
    st.markdown("<h1 class='sub-header'>Add a new Book</h1>", unsafe_allow_html=True)

    # adding book input form
    with st.form("add_book_form"):
        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input("Book Title",max_chars=100)
            author = st.text_input("Author", max_chars=100)
            publication_year = st.number_input("Publication Year", min_value=1900, max_value=datetime.now().year, step=1, value=2023)
        with col2:
            genre = st.selectbox("Genre", [
                "Fiction", "Non-Fiction", "Biography", "Mystery", "Thriller", "Fantasy", "Science Fiction", "Romance", "Horror", "Self-Help", "History", "Poetry", "Children's", "Young Adult", "Graphic Novel", "Cookbook", "Travel", "Science", "Philosophy", "Religion", "Comics", "Classic Literature","Professional", "Business", "Technology", "Health", "Sports", "True Crime", "Memoir", "Anthology", "Short Stories", "Essays", "Drama", "Adventure"
            ])
            read_status = st.radio("Read Status", ("Read", "Unread"), horizontal=True)   
            read_bool = read_status == "Read" 
        submit_button = st.form_submit_button("Add Book")

        if submit_button and title and author:
            add_book(title, author, publication_year, genre, read_bool)
          
    if st.session_state.book_added:
        st.markdown("<div class='sucess-message'>Book added successfully!</div>", unsafe_allow_html=True)  
        st.balloons
        st.session_state.book_added = False
elif st.session_state.current_view == "library":
    st.markdown("<h2class='sub-header'> Your Library</h2>", unsafe_allow_html=True)

    if not st.session_state.library:
        st.markdown("<div class='warning-message'>Your library is empty. Add some books to get started.</div>", unsafe_allow_html=True)
else:
    cols = st.columns(2)
    for i , book in enumerate(st.session_state.library):
        with cols[i % 2]:
            st.markdown(f"""<div class='book-card'>
                <h3>{book['title']}</h3>
                <p><strong>Author:</strong> {book['author']}</p>
                <p><strong>Publication Year:</strong> {book['publication_year']}</p>
                <p><strong>Genre:</strong> {book['genre']}</p>
                <p><span class='{'read-badge' if book['read_status'] else 'unread-badge'}'>{'Read' if book['read'] else 'Unread'}</span></p>
                </div>
                """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Remove", key=f"remove_{i}", use_container_width=True):
                   if  remove_book(i):
                       st.rerun()
            with col2:
                new_status = not book['read_status']
                status_label += "Mark as read" if not book['read_status'] else "Mark as unread"
                if st.button(status_label, key=f"status_{i}", use_container_width=True):
                   st.session_state.library[i]['read_status'] = new_status
                   save_library()
                   st.rerun()
    if st.session_state.book_removed:
        st.markdown("<div class='sucess-message'>Book removed successfully!</div>", unsafe_allow_html=True)  
        st.session_state.book_removed = False
    elif st.session_state.current_view == "search":
        st.markdown("<h2 class='sub-header'>Search Books</h2>", unsafe_allow_html=True) 

        search_by = st.selectbox("Search by", ("Title", "Author", "Genre"))
        search_term = st.text_input("Enter search term:")

        if st.button("Search", use_container_width=False):
            if search_term:
                with st.spinner("Searching..."):
                    time.sleep(0.5)
                    search_book(search_term, search_by)
        if hasattr(st.session_state, 'search_results'):
            if st.session_state.search_results:
                st.markdown(f"""
                            <div class='book-card'>
                            <h3>{book['title']}</h3>
                            <p><strong>Author:</strong> {book['author']}</p>
                            <p><strong>Publication Year:</strong> {book['publication_year']}</p>
                            <p><strong>Genre:</strong> {book['genre']}</p>
                            <p><span class='{'read-badge' if book['read_status'] else 'unread-badge'}'>{'Read' if book['read'] else 'Unread'}</span></p>
                            </div>
                """, unsafe_allow_html=True)
            elif search_term:
                st.markdown("<div class='warning-message'>No books found matching your search term.</div>", unsafe_allow_html=True)

    elif st.session_state.current_view == "statistics":
         st.markdown("<h2 class='sub-header'>Library Statistics</h2>", unsafe_allow_html=True) 

         if not st.session_state.library:
             st.markdown("<div class='warning-message'>Your library is empty. Add some books to get started.</div>", unsafe_allow_html=True)
         else:
             stats = get_library_state()
             col1,col2.col3 = st.columns(3)
             with col1:
                 st.metric("Total Books", stats['total_books'])
             with col2:
                 st.metric("Read Books", stats['read_books'])
             with col3:
                    st.metric("Percentage Read", f"{stats['percent_read']:.2f}%")
                    create_visulations()

                    if stats['authors']:
                        st.markdown("<h3>Top Authors</h3>", unsafe_allow_html=True)
                        for author, count in stats['authors'].items():
                            st.markdown(f"- {author}: {count} book{'s' if count > 1 else ''}")
st.markdown("---")
st.markdown("Copyright © 2025 M.HamzaKhan. All rights reserved.", unsafe_allow_html=True)                            
                   
             

# set page configuration
st.set_page_config(page_title="📚 Personal Library Management System", 
     page_icon="📖", 
    layout="wide",
    initial_sidebar_state="expanded")

# Sidebar Navigation
st.sidebar.markdown("<h1 style='text-align: center;'>📖 Navigation</h1>", unsafe_allow_html=True)
lottie_book = load_lottleurl("https://assets3.lottiefiles.com/packages/lf20_4j7v1g5h.json") 
if lottie_book:
    st_lottie(lottie_book, height=200, width=200, key="book animation")

nav_options = st.sidebar.radio(
    "Select an option",
    ["📚 View Library", "➕ Add Book", "🔍 Search Book", "📊 Statistics"])

# Main Header
st.markdown("<h1 class='main-header'>📚 Personal Library Management System</h1>", unsafe_allow_html=True)

# Add Book Section
if st.session_state.current_view == "add":
    st.markdown("<h1 class='sub-header'>➕ Add a New Book</h1>", unsafe_allow_html=True)

    # Adding book input form
    with st.form("add_book_form"):
        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input("📖 Book Title", max_chars=100)
            author = st.text_input("✍️ Author", max_chars=100)
            publication_year = st.number_input("📅 Publication Year", min_value=1900, max_value=datetime.datetime.now().year, step=1, value=2023)
        with col2:
            genre = st.selectbox("📚 Genre", [
                "Fiction", "Non-Fiction", "Biography", "Mystery", "Thriller", "Fantasy", "Science Fiction", "Romance", "Horror", "Self-Help", "History", "Poetry", "Children's", "Young Adult", "Graphic Novel", "Cookbook", "Travel", "Science", "Philosophy", "Religion", "Comics", "Classic Literature","Professional", "Business", "Technology", "Health", "Sports", "True Crime", "Memoir", "Anthology", "Short Stories", "Essays", "Drama", "Adventure"
            ])
            read_status = st.radio("📖 Read Status", ("✅ Read", "❌ Unread"), horizontal=True)   
            read_bool = read_status == "✅ Read" 
        submit_button = st.form_submit_button("➕ Add Book")

        if submit_button and title and author:
            add_book(title, author, publication_year, genre, read_bool)
          
    if st.session_state.book_added:
        st.markdown("<div class='sucess-message'>🎉 Book added successfully!</div>", unsafe_allow_html=True)  
        st.balloons()
        st.session_state.book_added = False

# View Library Section
elif st.session_state.current_view == "library":
    st.markdown("<h2 class='sub-header'>📚 Your Library</h2>", unsafe_allow_html=True)

    if not st.session_state.library:
        st.markdown("<div class='warning-message'>⚠️ Your library is empty. Add some books to get started.</div>", unsafe_allow_html=True)
    else:
        cols = st.columns(2)
        for i, book in enumerate(st.session_state.library):
            with cols[i % 2]:
                st.markdown(f"""<div class='book-card'>
                    <h3>📖 {book['title']}</h3>
                    <p><strong>✍️ Author:</strong> {book['author']}</p>
                    <p><strong>📅 Publication Year:</strong> {book['publication_year']}</p>
                    <p><strong>📚 Genre:</strong> {book['genre']}</p>
                    <p><span class='{'read-badge' if book['read'] else 'unread-badge'}'>{'✅ Read' if book['read'] else '❌ Unread'}</span></p>
                    </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🗑️ Remove", key=f"remove_{i}", use_container_width=True):
                        if remove_book(i):
                            st.rerun()
                with col2:
                    new_status = not book['read']
                    status_label = "✅ Mark as Read" if not book['read'] else "❌ Mark as Unread"
                    if st.button(status_label, key=f"status_{i}", use_container_width=True):
                        st.session_state.library[i]['read'] = new_status
                        save_library()
                        st.rerun()

    if st.session_state.book_removed:
        st.markdown("<div class='sucess-message'>🗑️ Book removed successfully!</div>", unsafe_allow_html=True)  
        st.session_state.book_removed = False

# Search Book Section
elif st.session_state.current_view == "search":
    st.markdown("<h2 class='sub-header'>🔍 Search Books</h2>", unsafe_allow_html=True) 

    search_by = st.selectbox("🔍 Search by", ("📖 Title", "✍️ Author", "📚 Genre"))
    search_term = st.text_input("🔍 Enter search term:")

    if st.button("🔍 Search", use_container_width=False):
        if search_term:
            with st.spinner("🔍 Searching..."):
                time.sleep(0.5)
                search_book(search_term, search_by)
    if hasattr(st.session_state, 'search_results'):
        if st.session_state.search_results:
            for book in st.session_state.search_results:
                st.markdown(f"""
                            <div class='book-card'>
                            <h3>📖 {book['title']}</h3>
                            <p><strong>✍️ Author:</strong> {book['author']}</p>
                            <p><strong>📅 Publication Year:</strong> {book['publication_year']}</p>
                            <p><strong>📚 Genre:</strong> {book['genre']}</p>
                            <p><span class='{'read-badge' if book['read'] else 'unread-badge'}'>{'✅ Read' if book['read'] else '❌ Unread'}</span></p>
                            </div>
                """, unsafe_allow_html=True)
        elif search_term:
            st.markdown("<div class='warning-message'>⚠️ No books found matching your search term.</div>", unsafe_allow_html=True)

# Statistics Section
elif st.session_state.current_view == "statistics":
    st.markdown("<h2 class='sub-header'>📊 Library Statistics</h2>", unsafe_allow_html=True) 

    if not st.session_state.library:
        st.markdown("<div class='warning-message'>⚠️ Your library is empty. Add some books to get started.</div>", unsafe_allow_html=True)
    else:
        stats = get_library_state()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📚 Total Books", stats['total_books'])
        with col2:
            st.metric("✅ Read Books", stats['read_books'])
        with col3:
            st.metric("📊 Percentage Read", f"{stats['percent_read']:.2f}%")
        create_visulations()

        if stats['authors']:
            st.markdown("<h3>✍️ Top Authors</h3>", unsafe_allow_html=True)
            for author, count in stats['authors'].items():
                st.markdown(f"- {author}: {count} book{'s' if count > 1 else ''}")

  
