import styles from './Autocomplete.module.css';
import  SearchIcon  from '@mui/icons-material/Search';
import { useRouter } from 'next/router';
import React, { useState } from 'react';
import Link from 'next/link';

function Autocomplete({ arr, setSelectedOpt }){
    
    function handleClick(option) {
        setSelectedOpt(option);
    }
  
    return(
        
        <div className={styles.list}>
            {   
                arr.lenght != 0 &&
                arr.map(opt => {
                    return  (
                       
                        <div className={styles.option} onClick={() => handleClick(opt)}>
                            <p>{opt}</p>
                        </div>
                        
                       
                    
                    );
                }
                    
                )
            }
        </div>
    );
  }
  
  
  export default Autocomplete;