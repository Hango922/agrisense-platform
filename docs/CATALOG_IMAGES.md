# Product catalog images

Reviewed assets live in `static/images/catalog/`. `catalog.json` maps product
names to local images and records source, artist and license. See `CREDITS.md`
in that folder for attribution. Photos illustrate the produce type, not proof
of a cultivar, geographic origin or supplier certification.

Apply to the local website:

```powershell
.venv/Scripts/python.exe manage.py refresh_catalog
```

The command replaces images for 20 existing products and adds 20 sample
products: vegetables, fruit, mushrooms, beans and nuts. New entries include
price, unit, sample stock, description, preparation and storage guidance.
Confirm prices and suppliers before real sales.

Repeated runs do not duplicate products or reset existing prices, inventory,
suppliers or active status. Matching normalizes case and Vietnamese accents
and never assumes database primary keys. No orders or accounts are created.
Images are copied to `MEDIA_ROOT/products/catalog-v2/`; existing files remain.
The listing, detail and cart templates all use the product's image field.

For the separate demo database, run after `seed_showcase`:

```powershell
.venv/Scripts/python.exe manage.py refresh_catalog --settings=nongsan_project.demo_settings
```

Operational settings reject this sample-data command.
`tools/fetch_product_images.py` now delegates to this command instead of
downloading images from the old primary-key-based URL mapping.
