## Toolbar Installation:
  1. Download the tarball.
  2. Open Coreform Cubit. 
  3. Go to Tools/Custom Toolbar Editor.
  4. Right click in the upper left frame labeled Toolbars.
  5. Select Import.
  6. Using the Package option, select the downloaded tarball and a destination directory.
  7. Click on the Import push button.
  8. Click on the Finish push button.

The gif illustrates the process. 
![import animation](assets/toolbar_import.gif)

## Creating an updated tarball
  1. Ensure that all changes to toolbar scripts are functioning in Cubit.
  2. Go to Tools/Custom Toolbar Editor.
  3. Right click in the upper left frame labeled Toolbars and Select Export.
  5. Select the export file location and name. The .tar.gz extension will be automatically added. The ... on the right hand side will open a file browser.
  6. Click on Next
  7. Check only the DAGMC toolbar and click Next.
  8. Click on Add Files. Browse into the scripts directory and select the __init__ and utils python files. 
  9. Click on Open. This will add a new folder called files.
  10. Open the files folder and drag __init__.py and utils.py into the scripts folder.
  11. Right click on the files folder and select Remove selected.
  12. Click on Finish.

## Usage
Once the toolbar is installed five new icons will be displayed in the Coreform Cubit toolbar.
![DAGMC toolbar image](assets/dagmc_toolbar.png)
The first icon presents an about box.
The second icon renames groups to a consistent naming convention
The third icon create Cubit blocks and materials from the group names.
The fourth icon provides a deviation report of the faceted geometry vs the CAD geoemtry.
The fifth icon reads an HDF5 results file and provides a visualization of lost particles and directions.

Once the model is defined you can export to DAGMC by either selecting the File/Export DAGMC option or typing at the command line "export dagmc 'filename.h5m'." Note that the quotation marks around the filename are required Cubit syntax.




