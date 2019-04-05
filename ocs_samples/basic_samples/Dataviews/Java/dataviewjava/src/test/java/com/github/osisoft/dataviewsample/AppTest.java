package com.github.osisoft.dataviewsample;


import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;


import org.junit.jupiter.api.Test;

import com.github.osisoft.ocs_sample_library_preview.*;
import com.github.osisoft.ocs_sample_library_preview.sds.*;
import com.github.osisoft.ocs_sample_library_preview.dataviews.*;

/**
 * Test for simple App.
 */
public class AppTest 
{
    @Test
    public void runMainProgram()
    {
        assertTrue( App.toRun() );
    }
    
}
