import styles from './UcaLogo.module.css';
import Image from 'next/image';
import logo from '../../../public/uca-logo.jpg';



function UcaLogo(){
  return(
    <div className={styles.wrapper}>
      
      <Image src={logo} width="300px" height="300px"/>


    </div>

  );
}


export default UcaLogo;