const MoreIotasCardinalComponents = Java.loadClass("ram.talia.moreiotas.fabric.cc.MoreIotasCardinalComponents")
const ChatHelper = Java.loadClass("org.sophia.slate_work.misc.ChatHelper")

let messages = []

ServerEvents.commandRegistry(event => {
    const { commands: Commands, arguments: Arguments } = event

    event.register(Commands.literal('queryMessages')
        .requires(s => s.hasPermission(4))
        .executes(c => {c.source.sendSystemMessage(JSON.stringify(messages)); messages = []}
      )
    )
  }
)

function toPython(data){
    messages.push(data)
}

function WillBlock(message, player){
    let hidden = false
    let prefix = MoreIotasCardinalComponents.CHAT_PREFIX_HOLDER.get(player).prefix
    if (prefix && message.startsWith(prefix)) {hidden = true}
    if (ChatHelper.getHelper().willBlock(message, player).blocked()) {hidden = true}
    return hidden
}

PlayerEvents.chat(event => {
    if (!WillBlock(event.message,event.player)){
        toPython([
            "CHAT",
            event.player.uuid.toString(),
            event.player.displayName.string,
            event.message,
            event.getComponent().toJson().toString()
        ])
    }
})

PlayerEvents.advancement(event => {
    if (event.advancement.advancement.display){
        if (event.advancement.advancement.display.shouldAnnounceChat()){
            toPython(["ADVANCEMENT",
                event.player.displayName.string,
                event.player.uuid.toString(),
                event.advancement.title.string,
                event.advancement.description.string
            ])
        }      
    }
    
})

PlayerEvents.loggedIn(event => {
    toPython(["JOIN", event.player.uuid.toString(),event.player.displayName.string])
})

PlayerEvents.loggedOut(event => {
    toPython(["LEAVE", event.player.uuid.toString(),event.player.displayName.string])
})

EntityEvents.death("player", event => {
    toPython(["DEATH", event.getSource().getLocalizedDeathMessage(event.getEntity()).string])
})

ServerEvents.loaded(event => {
    toPython(["CHAT", "hexxy","Hexxytest",'server started!', 0])
})