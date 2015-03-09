#!/usr/bin/env python

import logging
import math
import optparse

log = logging.getLogger( 'splitLHE' )


def main():
    usage = '%prog [options] LHEFILE'

    parser = optparse.OptionParser( usage=usage )
    parser.add_option( '-o', '--output', metavar='OUTPUTPREFIX', default='out',
                       help="Use OUTPUTPREFIX as prefix for the created output file. The filenames will be in the form of 'OUTPUTPREFIX_i.lhe' where 'i' is the file index. [default = %default]" )
    parser.add_option( '-N', '--Nevents', metavar='NEVENTS', type='int', default=10000,
                       help='Create files with (max.) NEVENTS per file. [default = %default]' )
    parser.add_option( '-n', '--Nfiles', metavar='NFILES', type='int', default=None,
                       help="Create (nominally) NFILES files. '--Nevents' is ignored in this case. [default = %default]" )
    parser.add_option(       '--debug', metavar='LEVEL', default='INFO',
                       help='Set the debug level. Allowed values: ERROR, WARNING, INFO, DEBUG. [default = %default]' )

    ( options, args ) = parser.parse_args()

    format = '%(levelname)s (%(name)s) [%(asctime)s]: %(message)s'
    date = '%F %H:%M:%S'
    logging.basicConfig( level=logging._levelNames[ options.debug ], format=format, datefmt=date )

    if len( args ) != 1:
        parser.error( 'Exactly one input LHE file needed!' )

    inFile = args[0]

    if options.Nfiles:
        options.Nevents = None

    splitter = Splitter( options )

    splitter.split( inFile )


class Splitter:
    def __init__( self, options=None ):
        if options:
            self.prefix = options.output
            self.Nevents = options.Nevents
            if self.Nevents:
                self.Nfiles = None
            else:
                self.Nfiles = options.Nfiles
        else:
            self.prefix = 'out'
            self.Nevents = 10000
            self.Nfiles = None

        self.output = self.prefix + '_%i.lhe'

    def split( self, inFile ):
        outFiles = []
        log.info( "Working on input file '%s'." % inFile )
        with open( inFile, 'r' ) as inputFile:
            eventCount = 0
            outFileCount = 0

            firstLine = None
            beginHeader = False
            endHeader = False
            beginInit = False
            endInit = False
            nEventsInFile = None
            beginEvents = False
            outFileOpen = False
            foundEnd = False
            ignore_line=False

            header = []
            init = []
            for line in inputFile:
                if not firstLine and '<LesHouchesEvents' in line:
                    log.info( 'File identified as LesHouchesEvents file.' )
                    log.debug( firstLine )
                    firstLine = line
                    # Everything before is ignored.
                    continue

                # Found the first event?
                if not beginEvents and '<event>' in line:
                    log.info( 'Found events in LHE file.' )
                    beginEvents = True

                if not beginEvents:
                    # Deal with the header:
                    if '<header>' in line:
                        log.info( 'Found header.' )
                        beginHeader = True
                    if '</header>' in line:
                        header.append( line )
                        log.debug( 'Full header:\n' + ''.join( header ) )
                        endHeader = True
                    if beginHeader and not endHeader:
                        #if 'nevents' in line and '=' in line:
                        if 'nevents' in line and '=' in line and "#" not in line:
                            nEventsInFile = int( line.split( '=' )[0].strip() )
                            if not self.Nevents:
                                self.Nevents = ( nEventsInFile / self.Nfiles ) + 1
                            if not self.Nfiles:
                                # This is only to get the output file names right!
                                self.Nfiles = int( math.ceil( float( nEventsInFile ) / float( self.Nevents ) ) )
                            self.updateOutput()

                        header.append( line )

                    # Init part:
                    if '<init>' in line:
                        log.info( 'Found init part.' )
                        beginInit = True
                    if '</init>' in line:
                        init.append( line )
                        log.debug( 'Full init:\n' + ''.join( init ) )
                        endInit = True
                    if beginInit and not endInit:
                        init.append( line )

                else:
                    if not outFileOpen:
                        outFileName = self.output % ( outFileCount + 1 )
                        log.debug( "Opening output file '%s'." % outFileName )
                        outFile = open( outFileName, 'w+' )
                        outFiles.append( outFileName )
                        outFileOpen = True
                        nextFile = False

                        print >> outFile, firstLine,
                        self.writeLines( header, outFile )
                        self.writeLines( init, outFile )

                    # End of LHE file?
                    if '</LesHouchesEvents>' in line:
                        foundEnd = True
                    else:
                        # Just count the processed events.
                        if '<event>' in line:
                            ignore_line=False
                            eventCount += 1
                        # Do we have enough events in this file?
                        if '</event>' in line and eventCount % self.Nevents == 0:
                            # Last event? No need for a new file then.
                            print >> outFile, line,
                            if eventCount == nEventsInFile:
                                nextFile = False
                            else:
                                nextFile = True
                    if "<scales" in line:
                        ignore_line=True

                    if ignore_line and not "</event>" in line:
                        #print line
                        #raw_input()
                        continue
                    print >> outFile, line,

                    if nextFile or foundEnd:
                        if nextFile:
                            log.debug( 'Event %i in file %i, going to next file' % ( eventCount, outFileCount ) )
                            # Write end of file flag.
                            print >> outFile, '</LesHouchesEvents>',
                        log.debug( "Closing outFile '%s'." % outFile.name )
                        outFile.close()
                        outFileOpen = False

                        if foundEnd:
                            log.info( 'Reached end of input file.' )
                            log.info( 'Found %i events in total.' % eventCount )
                            log.info( 'Created %i LHE files.' % ( outFileCount + 1 ) )
                            log.info( 'Done.' )
                            break

                        outFileCount += 1

        return outFiles

    def updateOutput( self ):
        # Append zeros to files depending on the total number of file created!
        # This makes it easier to handle the output.
        if self.Nfiles:
            # How many digits?
            length = len( str( self.Nfiles ) )
            self.output = self.prefix + '_%0' + str( length ) + 'i.lhe'

    def writeLines( self, lines, outFile ):
        for line in lines:
            print >> outFile, line,


if __name__ == '__main__':
    main()
