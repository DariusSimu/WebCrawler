from bs4 import BeautifulSoup
import requests

with open('mock_bookstore.html', 'r', encoding='utf-8') as f:
    doc = BeautifulSoup(f, 'html.parser')

print('Type 1 for all books, Type 2 for specific book, Type 3 to exit:')
choice = input('Enter your choice: ')

while choice != '3':
    listings = doc.find_all('div', class_='book-listing')
    match choice:
        case '1':
            print(f'Found {len(listings)} book listings:')
            for listing in listings:
                title = listing.find('a', class_='book-title').text.strip()
                author = listing.find('p', class_='book-author').text.strip()
                price = listing.find('p', class_='book-price').text.strip()
                print(f'Title: {title}, Author: {author}, Price: {price}')
            print('--- End of listings ---')
            choice = input('Enter your choice: ')
        case '2':
            title_query = input('Enter the book title to search for: ')
            for listing in listings:
                title = listing.find('a', class_='book-title').text.strip()
                if title_query.lower() in title.lower():
                    author = listing.find('p', class_='book-author').text.strip()
                    price = listing.find('p', class_='book-price').text.strip()
                    print(f'Found: Title: {title}, Author: {author}, Price: {price}')
            print('--- End of listings ---')
            choice = input('Enter your choice: ')
        case _:
            print('Invalid choice. Please enter 1, 2, or 3.')
            choice = input('Enter your choice: ')
print('Exiting...')