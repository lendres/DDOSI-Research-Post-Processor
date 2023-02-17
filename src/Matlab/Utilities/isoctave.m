function isOctave = isoctave()
    %ISOCTAVE Returns true if the environment is Octave.  Returns false if another
    #   environment is running (for example, Matlab).
    #
    %   ISOCTAVE = ISOCTAVE()

    isOctave                = exist("OCTAVE_VERSION", "builtin") ~= 0;
end
