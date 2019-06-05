import argparse, datetime, os, sys

import requests

def get_vendor_file(name,default_filename,default_url,header_comments,parse_function):
    kwargs = locals()
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f",default=default_filename,metavar="FILE",help="Specify the output {0} file.".format(name))
    parser.add_argument("-u",default=default_url,metavar="URL",help="Specify the URL to fetch the {0} data from.".format(name))
    parser.add_argument("-v",action="store_true",help="Give verbose progress messages.")
    args = parser.parse_args()
    line_number = 0
    # If the output filename already exists, rename it to filename.bak before
    # we create the new output file.
    if os.path.isfile(args.f):
        if args.v:
            print("Renaming {0} to {0}.bak".format(args.f))
        os.rename(args.f,args.f+".bak")
    # Fetch the content from the URL.
    if args.v:
        print("Fetching {0} data from {1}".format(name,args.u))
    res = requests.get(args.u)
    res.raise_for_status()
    if not res.content:
        print("Zero-sized response from from {0}".format(args.u))#file=sys.stderr))
        sys.exit(1)
    else:
        if args.v:
            print("Fetched {0} bytes".format(len(res.content)))
        with open(args.f,"w") as output_file:
            # Write the header comments to the output file.
            now = datetime.datetime.now()
            date_string = "{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}".format(now.year,
                                                                                   now.month,
                                                                                   now.day,
                                                                                   now.hour,
                                                                                   now.minute,
                                                                                   now.second)
            output_file.write(header_comments.format(date_string,args.u))
            line_number = parse_function(res,output_file,**kwargs)
        if args.v:
            print("{0} IAB entries written to file {1}.".format(line_number,args.f))
        
            
