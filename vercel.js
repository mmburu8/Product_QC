{
    "version": 2,
    "builds": [
      {
        "src": "Product_QC/wsgi.py",
        "use": "@vercel/python",
        "config": { "maxLambdaSize": "15mb", "runtime": "python3.11.5" }
      },
      {
        "src": "build_files.sh",
        "use": "@vercel/static-build",
        "config": {
          "distDir": "staticfiles_build"
        }
      }
    ],
    "routes": [
      {
        "src": "/static/(.*)",
        "dest": "/static/$1"
      },
      {
        "src": "/(.*)",
        "dest": "Product_QC/wsgi.py"
      }
    ]
  }