import Card from "../UI/Card";
import MealItem from "./MealItem/MealItem";
import classes from "./AvailableMeals.module.css";
import { useState, useEffect } from "react";

const AvailableMeals = () => {
  const [data, setData] = useState();
  const [recommendData, setRecommendData] = useState();
  const [CollabRecommend, setCollab] = useState();

  const apiUrl = "http://localhost:5000/";

  async function fetchAPI() {
    try {
      let response = await fetch(apiUrl);
      let output = await response.json();
      setData(output);

    } catch (err) {
      console.log("ERROR");
    }
  }

  console.log(data);
  useEffect(() => {
    fetchAPI();
    fetchRecommend();
    fetchCollab();
  }, []);


  async function fetchRecommend() {
    const recommendurl1 = "http://localhost:5000/api/contentbased?id=ACCEJWHTY2HVMG7Z5";
    const recommendurl2 = "http://localhost:5000/api/contentbased?id=JEAE9PP49AH6PQCW";

    try {
      let response1 = await fetch(recommendurl1);
      let output1 = await response1.json();

      let response2 = await fetch(recommendurl2);
      let output2 = await response2.json();
      setRecommendData([...output1,...output2]);

    } catch (err) {
      console.log("ERROR");
    }
  }

  async function fetchCollab() {
    const collaburl = "http://localhost:5000/api/collaborative?userid=1";

    try {
      let response = await fetch(collaburl);
      let output = await response.json();

      setCollab(output);

    } catch (err) {
      console.log("ERROR");
    }
  }

  const prodItem =
    data &&
    data.map((prod, index) => (
      <MealItem
        id={prod.pid}
        key={index + 1}
        name={prod.product_name}
        description={prod.brand}
        price={prod.retail_price}
      />
    ));

  const recommendItem = recommendData &&
    recommendData.map((prod, index) => (
      <MealItem
        id={prod.pid}
        key={index + 1}
        name={prod.product_name}
        description={prod.brand}
        price={prod.retail_price}
      />
    ));

    const Collab = CollabRecommend &&
    CollabRecommend.map((prod, index) => (
      <MealItem
        id={prod.pid}
        key={index + 1}
        name={prod.product_name}
        description={prod.brand}
        price={prod.retail_price}
      />
    ));

  return (
    <section className={classes.meals}>
      <h1 className={classes.heading}>Products</h1>
      <Card>
        <ul>{prodItem}</ul>
      </Card>
      <h1 className={classes.heading}>Recommended Products For You</h1>
      <Card>
        <ul>{recommendItem}</ul>
      </Card>
      <h1 className={classes.heading}>Similar Users Also Liked</h1>
      <Card>
        <ul>{Collab}</ul>
      </Card>
    </section>
  );
};

export default AvailableMeals;