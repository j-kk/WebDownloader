from API import factory

# Eventually force the environment
# factory.environment = 'default'

# Get flask instance
app = factory.flask

# Get celery instance
celery = factory.celery

if __name__ == '__main__':
    # Actually run the application
    app.run()