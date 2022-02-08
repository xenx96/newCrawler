import { Router } from "express";
import fs from "fs"
const router = Router();
/**
 * redirect와 Render를 주의해서 사용해주세요!
 *
 */

router.get("/", (req, res, next) => {
  res.redirect("/index");
});

router.get("/index", async(req, res, next) => {
  const imgArray = fs.readdirSync("./public/img","utf-8")
  imgArray.push("BB")
  res.render("index",{"text" : imgArray});
});


export default router;
