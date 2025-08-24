from django.contrib import admin

# Custom admin site configuration
admin.site.site_header = "Eduzen Admin"
admin.site.site_title = "Eduzen Admin"
admin.site.index_title = "Dashboard"

# Add custom links to the admin index
admin.site.index_template = "admin/custom_index.html"
