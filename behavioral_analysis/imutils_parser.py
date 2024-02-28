import argparse
from imutils.src import imfunctions
from imutils.src import unet_functions

FUNCTION_MAP = {'tiff2avi': imfunctions.tiff2avi,
                'ometiff2bigtiff': imfunctions.ometiff2bigtiff,
                'ometiff2bigtiffZ': imfunctions.ometiff2bigtiffZ,
                'max_projection_3d': imfunctions.max_projection_3d,
                'z_projection_parser': imfunctions.z_projection_parser,
                'stack_subtract_background': imfunctions.stack_subtract_background,
                'make_contour_based_binary': imfunctions.make_contour_based_binary,
                'unet_segmentation_stack': unet_functions.unet_segmentation_stack,
                'unet_segmentation_contours_with_children': imfunctions.unet_segmentation_contours_with_children,
                'erode': imfunctions.erode,
                'make_hyperstack_from_ometif': imfunctions.make_hyperstack_from_ometif,
                'stack_make_binary': imfunctions.stack_make_binary,
                'stack_normalise': imfunctions.stack_normalise,
                'images2stack': imfunctions.images2stack,
                'stack_extract_and_save_contours_with_children':imfunctions.stack_extract_and_save_contours_with_children
                }


# create the top-level parser
parser = argparse.ArgumentParser(prog='PROG')
# Just add the subparser, no need to add any other argument.
# Pass the "dest" argument so that we can figure out which parser was used.
subparsers = parser.add_subparsers(help='sub-command help', dest='subparser_name')

# create the parser for the "a" command
parser_a = subparsers.add_parser('tiff2avi', help='tiff2avi help')
# Keep the names here in sync with the argument names of the FUNCTION_MAP
parser_a.add_argument("-i", "--tiff_path", required=True, help="path to input tiff file")
parser_a.add_argument("-o", "--avi_path", required=True, help="path to output avi file")
parser_a.add_argument("-fourcc", "--fourcc", required=True, help="fourcc compression mode, 0 means no compression")
parser_a.add_argument("-fps", "--fps", required=True, help="Frames per second")

# create the parser for the "b" command
parser_b = subparsers.add_parser('ometiff2bigtiff', help='ometiff2bigtiff help')
parser_b.add_argument("-path", "--path", required=True, help="path to the input folder")
parser_b.add_argument("-output_filename", "--output_filename", required=False, help="output_filename string, should end with .btf")


# create the parser for the "c" command
parser_c = subparsers.add_parser('ometiff2bigtiffZ', help='ometiff2bigtiffZ help')
parser_c.add_argument("-path", "--path", required=True, help="path to the input folder")
parser_c.add_argument("-output_dir", "--output_dir", required=False, help="path to the output folder")
parser_c.add_argument("-actually_write", "--actually_write", required=False, help="True if you actually want to write")
parser_c.add_argument("-num_slices", "--num_slices", required=False, help="Number of slices your Z-Stack should have")

#parser for max_projection_3d
parser_d= subparsers.add_parser('max_projection_3d', help='max_projection_3d help')
parser_d.add_argument("-i", "--input_filepath", required=True, help="path to the input image")
parser_d.add_argument("-o", "--output_filepath", required=True, help="path to the output image")
parser_d.add_argument("-fold_increase", "--fold_increase", type=int)
parser_d.add_argument("-nplanes", "--nplanes", type=int)
parser_d.add_argument("-flip", "--flip", type=bool)

#parser for z_projection
parser_e= subparsers.add_parser('z_projection_parser', help='z_projection_parser help')
parser_e.add_argument("-i", "--hyperstack_filepath", required=True, help="path to the input image")
parser_e.add_argument("-o", "--output_filepath", required=True, help="path to the output image")
parser_e.add_argument("-type", "--projection_type", required=True, type=str, help="string containing the projection type")
parser_e.add_argument("-axis", "--axis", required=True, type=int, help="int or float containing the axis from which to make z projection")

#parser for stack_substract_background
# IMPORTANT! NOT SURE IT WORKS WITH THE INVERT!
parser_f= subparsers.add_parser('stack_subtract_background', help='stack_subtract_background help')
parser_f.add_argument("-i", "--input_filepath", required=True, type=str, help="path to the input image")
parser_f.add_argument("-o", "--output_filepath", required=True, type=str, help="path to the output image")
parser_f.add_argument("-bg", "--background_img_filepath", required=True, type=str, help="string with the background_img_filepath")
parser_f.add_argument("-invert", "--invert", required=True, type=bool, help="decide whether to invert or not the image")


#parser for make_contour_based_binary
parser_g= subparsers.add_parser('make_contour_based_binary', help='help')
parser_g.add_argument("-i", "--stack_input_filepath", required=True, help="path to the input image")
parser_g.add_argument("-o", "--stack_output_filepath", required=True, help="path to the output image")
parser_g.add_argument("-blur", "--median_blur", required=True, type=int, help="median blur that will be applied")
parser_g.add_argument("-th", "--threshold", required=True, type=float, help="threshold")
parser_g.add_argument("-max_val", "--max_value", required=True, type=float, help="new value of pixels above threshold")
parser_g.add_argument("-cs", "--contour_size", required=True, type=float, help="contour_size")
parser_g.add_argument("-t", "--tolerance", required=True, type=float, help="tolerance, percentage from which the contours can deviate from contour size")
parser_g.add_argument("-ics", "--inner_contour_area_to_fill", required=True, type=float, help="inner_contour_area_to_fill")

#parser for unet_segmentation_stack
parser_h= subparsers.add_parser('unet_segmentation_stack', help='unet_segmentation_stack')
parser_h.add_argument("-i", "--input_filepath", required=True, type=str, help="path to the input image")
parser_h.add_argument("-o", "--output_filepath", required=True, type=str, help="path to the output image")
parser_h.add_argument("-w", "--weights_path", required=True, type=str, help="string with the Unet weights filepath")


#parser for unet_segmentation_contours_with_children
parser_i= subparsers.add_parser('unet_segmentation_contours_with_children', help='unet_segmentation_contours_with_children help')
parser_i.add_argument("-bi", "--binary_input_filepath", required=True, type=str, help="path to the binary input image")
parser_i.add_argument("-ri", "--raw_input_filepath", required=True, type=str, help="path to the raw input image")
parser_i.add_argument("-o", "--output_filepath", required=True, type=str, help="path to the output image")
parser_i.add_argument("-w", "--weights_path", required=True, type=str, help="string with the Unet weights filepath")

#parser for eroding
parser_j= subparsers.add_parser('erode', help='erode help')
parser_j.add_argument("-i", "--binary_input_filepath", required=True, type=str, help="path to the binary input image")
parser_j.add_argument("-o", "--output_filepath", required=True, type=str, help="path to the output image")

#parser for make_hyperstack_from_ometif
parser_k= subparsers.add_parser('make_hyperstack_from_ometif', help='ake_hyperstack_from_ometif help')
parser_k.add_argument("-i", "--input_path", required=True, type=str, help="path to the input image")
parser_k.add_argument("-o", "--output_filepath", required=True, type=str, help="path to the output filepath")
parser_k.add_argument("-s", "--shape", required=True, type=tuple, help="shape")
parser_k.add_argument("-t", "--dtype", required=True, type=str, help="data type")
parser_k.add_argument("-imagej", "--imagej", required=True, type=bool, help="imagej")
parser_k.add_argument("-m", "--metadata", required=True, type=dict, help="metadata")

#parser for make_binary
parser_l= subparsers.add_parser('stack_make_binary', help='stack_substract_background help')
parser_l.add_argument("-i", "--stack_input_filepath", required=True, help="path to the input image")
parser_l.add_argument("-o", "--stack_output_filepath", required=True, help="path to the output image")
parser_l.add_argument("-th", "--threshold", required=True, type=float, help="threshold")
parser_l.add_argument("-max_val", "--max_value", required=True, type=float, help="max value that will be assigned")

#parser for stack_normalise
parser_m= subparsers.add_parser('stack_normalise', help='stack_normalise help')
parser_m.add_argument("-i", "--stack_input_filepath", required=True, help="path to the input image")
parser_m.add_argument("-o", "--stack_output_filepath", required=True, help="path to the output image")
parser_m.add_argument("-a", "--alpha", required=True, type=float, help="min")
parser_m.add_argument("-b", "--beta", required=True, type=float, help="max")

#parser for images2stack
parser_n= subparsers.add_parser('images2stack', help='images2stack help')
parser_n.add_argument("-p", "--path", required=True, help="path to folder")
parser_n.add_argument("-o", "--output_filename", required=True, help="path to the output file")

#parser for stack_extract_and_save_contours_with_children
parser_o = subparsers.add_parser('stack_extract_and_save_contours_with_children', description='Description of your program')
parser_o.add_argument('-bi', '--binary_input_filepath', help='binary input filepath', required=True)
parser_o.add_argument('-ri', '--raw_input_filepath', help='raw input filepath', required=True)
parser_o.add_argument('-o', '--output_folder', help='output folder', required=True)
parser_o.add_argument('-ct', '--crop', action='store_true', help='set crop to True', required=False)
parser_o.add_argument('-s', '--subsample', help='subsample', type=int, required=False)

#create below the parser for another function


#parse args
args = parser.parse_args()

# subparser_name has either "tiff2avif" or "ometiff2bigtiff".
func = FUNCTION_MAP[args.subparser_name]
# the passed arguments can be taken into a dict like this
func_args = vars(args)
# remove "subparser_name" - it's not a valid argument
del func_args['subparser_name']
# now call the function with its arguments
func(**func_args)
