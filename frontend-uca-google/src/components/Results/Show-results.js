
import Results from './Results';
//import datos from './datos.json';
import styles from './Results.module.css';

function Show_results(props){
  return(
    <div>
    {
      props.datox.results.map(dato =>{
        return(
          <Results
          title={"Lorem Ipsum"}
          link={dato.url}
          description={"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. I"}
        />
        )
      })
    }

    </div>

  );

}

export default Show_results;
