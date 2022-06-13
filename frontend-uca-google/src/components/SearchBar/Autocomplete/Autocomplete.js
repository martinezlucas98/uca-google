import styles from './Autocomplete.module.css';
import  SearchIcon  from '@mui/icons-material/Search';
import { useRouter } from 'next/router';
import React, { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { red } from '@mui/material/colors';

function Autocomplete({ arr, setSelectedOpt, focus, onClickOutside, show}){
    const ref = useRef(null)

    function handleClick(option) {
        setSelectedOpt(option);
    }
    useEffect(() => {
        const handleClickOutside = (event) => {
            if(ref.current && !ref.current.contains(event.target)){
                onClickOutside && onClickOutside()
            }
        };
        document.addEventListener('click', handleClickOutside, true);
        return() => {
            document.removeEventListener('click', handleClickOutside, true);
        };
    }, [onClickOutside]);

    if(!show){
        return null;
    }
    
    return(
        
        <div ref={ref} className={styles.list}>
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