
import styles from './Results.module.css';
import Link from 'next/link';

function Results(props){

  return(
    <Link href={'https://' + props.link} passHref>
      <a>
    
          <div className={styles.container}>
                
                <div className={styles.wrapper}>

                  <p className={styles.title}> Title = {props.title}</p>
                  <p className={styles.link}> Link = {props.link}</p>
                  <p className={styles.description}> Descripcion = {props.description}</p>
                
                </div>
          
          </div>
        </a>
      </Link>
    
   

  );
}

export default Results;

