import nibabel as nib
import vtk

img1 = nib.load('image_lr.nii')
img1_data = img1.get_fdata()
dims = img1.shape
spacing = (img1.header['pixdim'][1],img1.header['pixdim'][2],img1.header['pixdim'][3])

image = vtk.vtkImageData()
image.SetDimensions(dims[0],dims[1],dims[2])
image.SetSpacing(spacing[0],spacing[1],spacing[2])
image.SetOrigin(0,0,0)

if vtk.VTK_MAJOR_VERSION <= 5:
    image.SetNumberOfScalarComponents(1)
    image.SetScalarTypeToDouble()
else:
    image.AllocateScalars(vtk.VTK_DOUBLE,1)

for z in range(dims[2]):
    for y in range(dims[1]):
        for x in range(dims[0]):
            scalarData = img1_data[x][y][z]
            image.SetScalarComponentFromDouble(x,y,z,0,scalarData) 

Extractor = vtk.vtkMarchingCubes()
Extractor.SetInputData(image)
Extractor.SetValue(0,150)

smoother = vtk.vtkSmoothPolyDataFilter()
smoother.SetInputConnection(Extractor.GetOutputPort())
smoother.SetNumberOfIterations(1000)

stripper = vtk.vtkStripper()
stripper.SetInputConnection(smoother.GetOutputPort())

mapper = vtk.vtkPolyDataMapper() 
mapper.SetInputConnection(stripper.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

actor.GetProperty().SetColor(1,1,0)
actor.GetProperty().SetOpacity(0.95)
actor.GetProperty().SetAmbient(0.05)
actor.GetProperty().SetDiffuse(0.5)
actor.GetProperty().SetSpecular(1.0)

ren = vtk.vtkRenderer()
ren.SetBackground(1,1,1)
ren.AddActor(actor)
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(750,750)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
renWin.Render()
iren.Start()