<script lang="ts">
import LevelFilenameList from "@/components/LevelFilenameList.vue";
import { defineComponent } from "vue";

export default defineComponent({
  components: { LevelFilenameList },
  data() {
    return {
      levelsTr1: [
        ["LEVEL1", "Caves"],
        ["LEVEL2", "City of Vilcabamba"],
        ["LEVEL3A", "Lost Valley"],
        ["LEVEL3B", "Tomb of Qualopec"],
        ["LEVEL4", "St. Francis' Folly"],
        ["LEVEL5", "Colosseum"],
        ["LEVEL6", "Palace Midas"],
        ["LEVEL7A", "The Cistern"],
        ["LEVEL7B", "Tomb of Tihocan"],
        ["LEVEL8A", "City of Khamoon"],
        ["LEVEL8B", "Obelisk of Khamoon"],
        ["LEVEL8C", "Sanctuary of the Scion"],
        ["LEVEL10A", "Natla's Mines"],
        ["LEVEL10B", "Atlantis"],
      ],
      levelsTr1UB: [
        ["EGYPT", "Return to Egypt"],
        ["CAT", "Temple of the Cat"],
        ["END", "Atlantean Stronghold"],
        ["END2", "The Hive"],
      ],
    };
  },
});
</script>

<template>
  <div class="about-container">
    <h3>What is this all about?</h3>
    <p>
      This is a web service to play in coop with others using
      <a href="https://github.com/stohrendorf/CroftEngine" target="_blank"
        >CroftEngine</a
      >. The coop feature allows you to see other players which are within the
      same session as you, yet you will not be able to interact with each other.
      It is only a visual feature, which can be used to learn techniques from
      others, or for speedrunning challenges.
    </p>

    <h3>
      What about my privacy? Will you sell my data? Will I get random e-mails
      from you?
    </h3>
    <p>
      Not at all. Your privacy is very important, yet we require you to
      authenticate with a legit e-mail address. The reason for this is because
      there were a few individuals joining the community which were behaving
      badly, invading other peoples' freedom. Sadly, we <em>need</em> the
      possibility to ban some people.
    </p>
    <p>
      Only very few select people will see your e-mail address, and nobody else.
      These few select people are here to protect the community, and they need
      access to some account details to correctly identify individuals who are
      behaving badly.
    </p>
    <p>
      There's no way for us to prove this, unfortunately. You have to decide
      yourself whether you trust us.
    </p>

    <h4>Do you use cookies?</h4>
    <p>
      Yes, but this site only uses only cookies necessary for the site to
      function. There are no analytics cookies or tracking cookies.
    </p>

    <h3>How do I join a coop session?</h3>
    <p>
      It's pretty simple. Don't get afraid of the lengthy explanation, as we try
      to cover every detail. Once you get the hang of it, it's really simple.
    </p>
    <ol>
      <li>
        Create an account by clicking the &ldquo;Login/Register&rdquo; dropdown
        on the top right of this page, and then click on &ldquo;Register&rdquo;.
      </li>
      <li>
        Enter your desired username, an e-mail address you have access to, and a
        password for this site. Then click on &ldquo;Register&rdquo;. If there's
        any issue with the information you entered in this form, you will be
        informed, and have the chance to fix the issue.
      </li>
      <li>
        You will then receive an e-mail at the address you specified. Within,
        there's a link you need to click, which is necessary to confirm that you
        have access to the e-mail address you provided.
      </li>
      <li>
        After that, you need to log in with your username and your password.
        Make sure you use the proper casing for your username.
      </li>
      <li>
        Once logged in, your username shows up in the upper right corner of the
        page. To the left of it, you'll find a new dropdown titled
        &ldquo;Session Credentials&rdquo;. When you click on it, it will show
        you most of the information you need to enter into CroftEngine's
        launcher in the &ldquo;Configuration&rdquo; tab.<br />
        You can use the blue clipboard buttons to copy the values to your
        clipboard, and then you can use <kbd>Ctrl+V</kbd> to paste these values
        into the corresponding inputs of the launcher.
      </li>
      <li>
        The only thing left is to fill in the &ldquo;Session ID&rdquo;. Go to
        the &ldquo;Sessions&rdquo; tab at the top of the site, and select a
        session you want to join. Copy the session ID using the blue clipboard
        symbol, and paste it into the corresponding field in the launcher.
      </li>
      <li>
        Now you're ready to go. Launch a game, and if you're lucky, get haunted
        by some ghosts.
      </li>
    </ol>

    <h3>I want to create my own session for my friends.</h3>
    <p>
      By using the &ldquo;Create Session&rdquo; section of this site, you can
      create sessions on your own.
    </p>
    <ol>
      <li>
        Enter an optional description if you want to. You can leave this field
        empty, but we recommend to give a short description about your session's
        goals if it's publicly listed.
      </li>
      <li>
        Check whether you want your session to be publicly visible, or if you
        prefer a private session. If you prefer to create a private, or
        unlisted, session, you will need to share your session ID on your own,
        because nobody except you will see the session listed.
      </li>
      <li>
        If you want to tell people that your session is for a time-scoped event,
        for example a speedrun, you can check the &ldquo;Scheduled Event&rdquo;
        checkmark, which allows you to specify the time frame for the event.
        This time frame will be visible in the Sessions list.
      </li>
      <li>
        Check all the tags that apply to your session if you want to. We highly
        recommend to use the proper tags for publicy listed sessions, because it
        helps people decide which session is right for them.
      </li>
      <li>
        Click &ldquo;Create&rdquo;, and you're done. Your session now shows up
        in the &ldquo;Sessions&rdquo; list, and you will be able to edit it or
        delete it afterwards.
      </li>
    </ol>
    <p>
      Please note that your session will get deleted automatically if it is not
      used by any player for some time.
    </p>

    <h3>What are these &ldquo;Ghosts&rdquo;?</h3>
    <p>
      These are based on the same technology as the Coop ghosts, but they are
      only stored on your local PC, and nobody else will see your ghosts unless
      you share your ghost files. Your local ghost is always blue, and never has
      a name above its head.
    </p>
    <p>
      You can use these ghosts, for example, to challenge another ghost shared
      in the &ldquo;Ghosts&rdquo; section of this site, or download a tutorial
      or walkthrough ghost to learn more about some level.
    </p>

    <h3>How do I share my Ghost? Because my Ghost is awesome!</h3>
    <p>
      First, locate your ghost file. Within the CroftEngine launcher, go to the
      &ldquo;Configuration&rdquo; tab, and click on &ldquo;Show Data
      Location&rdquo;. This will open your file explorer. If you have any saved
      ghosts, there will be a folder named <code>ghosts</code>. Within there, go
      into folder for the game you recorded a ghost for (for example,
      <code>tr1</code> for Tomb Raider 1). In this folder, you will see a few
      files named like <code>LEVEL1</code>, <code>LEVEL2</code>, etc., which are
      your recorded ghosts.
    </p>
    <blockquote>
      Note: As of right now, these are the level filenames, and not the actual
      level titles. A list of level filenames and their respective levels is at
      the bottom of this page.
    </blockquote>
    <p>
      You can now drag and drop the <code>.xz</code> file of the ghost you want
      to share in the &ldquo;Upload Ghosts&rdquo; section. Then click
      &ldquo;Upload&rdquo;, and fill in the details about your
      ghost&mdash;select the level and game from the dropdown, select the tags
      that match your ghost, and don't forget to check the &ldquo;Publish&rdquo;
      checkmark (it's somewhat hidden between the dropdown and the tags list).
    </p>

    <h3>How do I download and use a Ghost?</h3>
    <p>
      Go to the &ldquo;Ghosts&rdquo; section of this site, and look for a ghost
      you want to see in your game. When you click on the link in the
      &ldquo;Level&rdquo; column, it will download a
      <code>.bin</code> file, which contains the ghost data. Save this into your
      ghosts folder, which you can find by following the instructions above. If
      you are asked whether you want to overwrite a file, say &ldquo;Yes&rdquo;.
    </p>
    <p>
      Please note that downloaded ghosts <em>will become your local ghost</em>.
      If you want to keep the downloaded ghost,
      <em>do not say &ldquo;Yes&rdquo;</em> when asked whether to save your
      recorded ghost. Otherwise, your own ghost will replace the ghost you
      downloaded.
    </p>

    <h3>
      This Ghost sharing is very complicated. I don't have a degree in Computer
      Science!
    </h3>
    <p>
      We are aware this ghost sharing stuff is not exactly user-friendly, but as
      demand is very very low at the moment, priorities are focused on fixing
      bugs and improve gameplay. Once there's time for working on this, it will
      eventually be improved and get a proper integration within the launcher.
    </p>

    <h3>Level Names and their corresponding filenames</h3>

    <h4>Tomb Raider 1 and Sabatu's Tomb Raider</h4>
    <level-filename-list
      game="Tomb Raider 1 and Sabatu's Tomb Raider"
      :levels="levelsTr1"
    />

    <h4>Tomb Raider 1&mdash;Unfinished Business</h4>
    <level-filename-list
      game="Tomb Raider&mdash;Unfinished Business"
      :levels="levelsTr1UB"
    />
  </div>
</template>

<style scoped>
h3 {
  position: relative;
  margin-left: -1.333em;
}

div.about-container {
  margin-left: 2.333em;
}
</style>
