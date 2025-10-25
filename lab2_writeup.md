## Lab 2 WriteUp

### A. Integrating Genai Features and UI Optimization
- **UI Color Palette Tuning**
    The original note interface had a purple background that somewhat resembled an AI-generated look. To solve this problem, I quickly used Copilot to change the entire interface's color to a more neutral and softer tone, optimizing the overall visual experience.
    ![界面颜色更改](./lab2_images/uicolor_change.png)

- **Adding Tag Recording Date and Time to Notes**
I started by adding components for tags, date, and time recording to the notes, but encountered an error during testing. I troubleshooted and realized this was because the frontend interface had been modified, but the backend database structure (or table) was not updated simultaneously. After unifying the front-end and back-end structures, these new recording features were successfully implemented.
    ![添加tag功能组件](./lab2_images/add_tag.png)

    The development process for integrating date and time components within the note structure.
    ![添加time和date功能组件](./lab2_images/add_timedata.png)

    The image below displays the entire database modification process and the structure of the resulting table.
    ![数据库修改](./lab2_images/database_change.png)
    The database table shows the implemented modifications.
    ![数据库修改](./lab2_images/database_change2.png)

- **Users Dragging Functionality for Note List Order**
The implementation of the drag-and-drop sorting feature was primarily completed using prompts from Copilot to generate the core drag and drop logic. However, after running the code, the project continuously threw errors. Upon inspection, I found that the dotenv dependency package was missing. After reinstalling the package and updating the project's requirements, the drag-and-drop sorting functionality was successfully implemented.
    ![推拽功能实现](./lab2_images/drag_drop.png)
    ![dotenv依赖安装](./lab2_images/dotenv.png)

- **Core Function Refinement and Issue Resolution**
Before jumping into adding the GenAI features, I decided to first address and fix the issues I found existing in the app.
    ##### Title Length Limit
    When adding a note in the app, I found that the note title had no length limit. This was not only unreasonable but, more importantly, caused the page UI layout to be disrupted. Therefore, I limited the note title length to within 20 characters.
    ![标题长度限制](./lab2_images/title_limit.png)

    ##### Undolist UI Bug Resolution
    During application testing, I found a very obvious UI issue: when clicking on an element in the Undo List, a black border appeared at the bottom of the list item. I modified the UI styles for this section, successfully removing the extra border and ensuring visual consistency.
    ![undolist的ui问题](./lab2_images/beforefix_undolist.png)
    As shown in the image, this border issue was clearly visible. To quickly resolve this UI defect, I adjusted the relevant styles with assistance from Copilot.
    ![undolist的ui问题修复](./lab2_images/fix_undolist.png)
    The resulting interface view after the fix.
    ![undolist的ui问题修复之后](./lab2_images/afterfix_undolist.png)

    ##### Note Date Picker Functionality Fix
    In the initial implementation, the note date picker allowed users to select any date. Considering the reasonableness of note-taking, I believed this selection logic was inappropriate. Therefore, with assistance from Copilot, I modified the date selection range to restrict choices to only the current day and future dates, thereby ensuring the correctness of the business logic.
    ![笔记日期选择器功能修复](./lab2_images/data_chancefix.png)
    ![笔记日期选择器功能修复之后](./lab2_images/data_change.png)
     Furthermore, I observed that while other application components were displayed in English, this specific date picker component was rendered in Chinese. To maintain consistent interface language, I further modified the component to its English version.
     ![笔记日期选择器组件英文](./lab2_images/data_english.png)

    ##### Note Saving Functionality Fix
    This bug significantly impacted the core functionality of the notes. Utilizing guidance and assistance from Copilot, I successfully fixed the issue where modified notes could not be saved.
    ![笔记可修改](./lab2_images/save_change.png)


### B. AI Feature Integration
Having completed the foundational features and fixed various bugs (such as UI color tuning and resolving the save issue), we will now proceed with integrating the GenAI functionality. These preliminary fixes have made the app more complete, and I can now start incorporating smart features like automatic translation and note generation, making this note-taking application even smarter.
- **Add GenAI's translation function**
First, I created a dedicated llm.py file for interface testing. By referencing the GPT-4.1 API method retrieved from the GitHub model repository, I successfully completed the API interface call and functionality verification. Furthermore, to prevent the key from leaking when synchronizing to GitHub, I took specific measures to ensure the API key was stored in a .env file during this step.
![引入ai进行翻译功能测试](./lab2_images/translate.png)
With the ability to call the gpt4.1mini translation API, I instructed Copilot to integrate a one-click translation feature into the Note App, utilizing the custom llm.py file I had written to handle the translation logic. This process successfully enabled the end-to-end integration of the frontend and backend translation functionality.
![翻译功能集成](./lab2_images/translate_integration.png)
As shown in the image, the main text was translated, but the note title was not. Further optimization was required to ensure that the title could also be translated with a single click.
![翻译功能优化](./lab2_images/translate_title.png)

- **Add Note Generation function**
Using a similar methodology, I first implemented the corresponding GenAI functions within llm.py to extract tags and generate content based on the title. After successful testing, I immediately utilized Copilot to integrate the Note Generation functionality into the application.
![笔记生成函数集成](./lab2_images/note_generate.png)
![笔记生成函数集成](./lab2_images/note_generatefix.png)
Although the note generation function was initially implemented, I observed that the date and time fields were not automatically populated in the generated notes. My next step is to refine the code to ensure these critical metadata points are synchronously updated.
![笔记生成问题](./lab2_images/note_generate_apply.png)
After fixing the automatic date and time population issue, I discovered that the feature could not provide specific date population for natural language expressions such as "tomorrow," "the day after tomorrow," or "11.2." Consequently, I also implemented optimizations for this problem.
As shown in the comparative images below, the optimized generation function accurately parses the natural language term "tomorrow" and automatically populates the specific date.
![笔记日期修复之前](./lab2_images/note_generate_before.png)
![笔记日期修复之后](./lab2_images/note_generate_after.png)


### C. Cloud Persistence Refactoring using Supabase
As I was unfamiliar with the deployment process, I leveraged Copilot to generate the necessary deployment steps, as illustrated in the figure below.
![部署步骤生成](./lab2_images/step2deploy.png)
I followed the deployment plan provided by Copilot, beginning by downloading all necessary libraries and updating the requirements.txt file. Subsequently, I registered on the Supabase platform and successfully created and configured the new PostgreSQL database.
![supabase设置](./lab2_images/database_setting.png)
Subsequently, I designed and created the necessary table structure in Supabase and successfully completed the debugging process.
![supabase表结构](./lab2_images/database_table.png)
Then, I configured the relevant keys and APIs, successfully linked the Supabase instance, and thereby established the connection to the cloud database.
![supabase链接](./lab2_images/supabase_link.png)

I began testing this section and observed that the frontend was successfully sending the note to the backend; however, Supabase did not receive it, resulting in an error.
![前端上传成功](./lab2_images/frontend_ok.png)
![后端报错](./lab2_images/backend_error.png)
This was puzzling; after careful troubleshooting, I ultimately discovered that the error was caused by a mismatch between the Supabase table schema and the data format being sent from the frontend.
After successfully resolving the Supabase table schema mismatch error, the database migration work was completed. I will now proceed to the next critical stage: Vercel deployment.

### D. Vercel Deployment
I registered a Vercel account and utilized its feature to import the project directly from the GitHub repository, quickly completing the project configuration and initial deployment attempt.
![vercel部署](./lab2_images/vercel_deploy1.png)
![vercel部署](./lab2_images/vercel_deploy2.png)
![vercel部署](./lab2_images/vercel_deploy3.png)
I meticulously followed every configuration step prompted by Copilot, and upon seeing the "Congratulations" success message, I initially believed the deployment was complete. However, upon access, the webpage returned a 500 Internal Server Error. I spent a considerable amount of time debugging and troubleshooting the issue.
![vercel部署](./lab2_images/vercel_deploy4.png)
![vercel部署](./lab2_images/vercel_deploy5.png)
I reviewed the run log and found that the error pointed to a file opening issue on line 50 of main.py. I modified the code, pushed the changes to Git, and redeployed on Vercel, but the deployment was still unsuccessful.
I confirmed that the code on the Git branch linked to Vercel was definitely modified, yet the redeployment still showed the exact same error in the logs. Upon checking the project code on Vercel, I realized its version had not been updated, which was extremely peculiar and made me consider abandoning the deployment altogether.
I later realized that my GitHub repository was private, and the Vercel free tier only supports public repositories. When I attempted to change it to public, I discovered that this was a branch of the instructor's class project and could not be edited. Consequently, I created a new public repository, pushed the project to it, and successfully deployed from there.
![vercel部署成功](./lab2_images/vercel_deploy_success.png)
![vercel部署成功](./lab2_images/vercel_deploy_success2.png)
Finally, I successfully completed the Vercel deployment and pushed the latest project code to the GitHub repository. This lab is now complete!

## conclusion
In this lab, I integrated GenAI into the note-taking app, fixed the date-constraint and save bugs, rebuilt the Supabase persistence layer, and deployed the app on Vercel. It was a lot of trial and error—deployment was new to me—so this lab gave me a great chance to sharpen my end-to-end engineering skills. It was challenging, but also a lot of fun.






