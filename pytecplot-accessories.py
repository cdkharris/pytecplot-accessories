"""
pytecplot-accessories
a bunch of more-or-less useful functions for working with tecplot through python
"""
import tecplot

def load_layout_save(layout_path,save_path,annotation=''):
    """
    Load a layout and save the image. Option to add an annotation in the upper
    left corner of the figure.
    Useful when the layout references a file with relative paths.
    E.G. if the layout loads a file called "./data.plt" then you can copy the
    layout into any directory which has a file named "./data.plt". Then use this
    function to make a plot of that data.

    Keyword Arguments
    ---
    layout_path: the path to the layout file
    save_path  : the pathname of the image to save (png)
    annotation : (optional) a string which will be printed in the upper left
                 corner of the plot
    """
    tecplot.load_layout(layout_path)
    frame = tecplot.active_frame()
    frame.add_text(annotation,position=(7,93), size=20)
    tecplot.export.save_png(save_path,width=1200,supersample=8)
    print('Saved '+save_path)


def load_eqn_frame_save(dataset_path,eqn_path,frame_styles,save_paths,annotation=''):
    """
    Load the data, run an equations file, run a set of frame styles, and export
    the plots.
    Keyword Arguments
    ---
    dataset_path: the path to the dataset (plt)
    eqn_path    : the path to the equation macro file (eqn)
    frame_styles: a list of the paths to the frame style files (sty)
    save_paths  : a list of the pathnames of the images to save (png)
    annotation  : (optional) a string which will be printed in the upper left
                  corner of the plots
    """
    ## load the data
    tp_data = tecplot.data.load_tecplot(dataset_path,read_data_option=tecplot.constant.ReadDataOption.Replace)
    print('Loaded ' + dataset_path)
    ## parse and run these equations
    print('Executing:')
    with open(eqn_path,'r') as f:
        eqns = ''
        for line in f:
            if line[0] == ' ':
                eqnstr = line.split("'")[1]
                tecplot.data.operate.execute_equation(eqnstr)
                print(eqnstr)
    print('Successfully applied equations')
    for i in range(len(frame_styles)):
        ## apply frame styles
        frame = tecplot.active_frame()
        frame.load_stylesheet(frame_styles[i])
        frame.add_text(annotation,position=(7,93), size=20)
        print('Applied '+frame_styles[i])
        ## export the plot
        tecplot.export.save_png(save_paths[i],width=1200,supersample=8)
        print('Saved '+save_paths[i])
