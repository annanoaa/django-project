# Django Store and Order Project

## Project Overview

This project is a Django-based web application that includes two main apps:
- **Store**: Manages products and categories with a tree-like category structure and allows products to belong to multiple categories.
- **Order**: Manages order-related features (currently under development).

The project also provides API views for returning categories and products in JSON format. It supports handling product images with media files stored locally.

## Features

### Store App:
- **Category Management**: Categories can be arranged in a tree-like hierarchy, and a category can have multiple child categories.
- **Product Management**: Products can belong to multiple categories and include product images.
- **JSON API**:
  - `GET /store/categories/`: Returns all categories along with their parent categories (first level only).
  - `GET /store/products/`: Returns a list of products along with their immediate parent categories.

### Order App:
- (To be implemented)

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject
