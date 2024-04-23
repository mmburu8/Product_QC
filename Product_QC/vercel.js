{
    "build": [
        {"src": "Product_QC/wsgi.py",
    "use": "@vercel/python"},
    ],
    "routes": [
        {
            "src": "/(.*)",
            "dest": "Product_QC/wsgi.py"
        }
    ]
}